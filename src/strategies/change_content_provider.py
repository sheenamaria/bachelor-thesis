import re

from src.core.utils import group_by
from src.store.mdb_store import db, Collection
from src.strategies.defs import IContentStrategy, ICommitInfo
from src.tasks.pipeline_context import PipelineContext


class ChangeContentProvider:
    def get_content(
        self, context: PipelineContext, content_strategy: IContentStrategy
    ) -> [ICommitInfo]:
        if isinstance(content_strategy, dict):
            return self._get_content(context, content_strategy)
        elif isinstance(content_strategy, list):
            contents = []
            for cs in content_strategy:
                content = self._get_content(context, cs)
                contents.extend(content)
            content_groups = group_by(contents, "commit_hash")
            commit_infos = []
            for key, items in content_groups.items():
                commit_info = items[0]
                commit_info["resources"] = [commit_info["resource"]]
                for item in items[1:]:
                    commit_info["change_text"] = "\n".join(
                        [commit_info["change_text"], item["change_text"]]
                    )
                    commit_info["filename"] = ", ".join(
                        [commit_info["filename"], item["filename"]]
                    )
                    commit_info["resources"].append(item["resource"])
                commit_infos.append(commit_info)
            return commit_infos
        else:
            raise RuntimeError(
                "ChangeContentProvider.get_content - unsupported content strategy"
            )

    def _get_content(
        self, context: PipelineContext, content_strategy: IContentStrategy
    ) -> [ICommitInfo]:
        file_type = "text"
        if content_strategy["terms"] == "meta_ast_code":
            file_type = "java"

        criteria = context.create_resource_criteria(
            {
                "strategy.meta": content_strategy["meta"],
                "kind": "term",
                "type": file_type,
                "strategy.terms": content_strategy["terms"],
            }
        )
        change_resources = db.find_resources(criteria)
        commit_infos: [ICommitInfo] = []
        for change_resource in change_resources:
            commit_info = self._get_commit_info(context, change_resource)
            if commit_info is not None:
                commit_infos.append(commit_info)
        return commit_infos

    def _get_commit_info(
        self, context: PipelineContext, change_resource
    ) -> ICommitInfo:
        change_content = db.get_resource_content(change_resource, volatile=True)
        change_text = change_content.strip() if change_content else ""
        commit = db.find_object(change_resource.get("@container"))
        pull_request_title = commit.get("pull_request_title", "")
        pull_request_text = commit.get("pull_request_text", "")
        issue_text = ""
        numbers = [int(d) for d in re.findall(r"\d+", pull_request_title)]
        if len(numbers):
            issues = list(
                Collection.github_issue.find(
                    context.create_issue_criteria({"number": {"$in": numbers}})
                )
            )
            issue_items = []
            for issue in issues:
                issue_items.append(issue["title"])
                # issue_items.append(issue["bodyText"])
            issue_text = " ".join(issue_items)

        pull_request_text = " ".join(
            [pull_request_title, pull_request_text, issue_text]
        )
        commit_info = {
            "commit_hash": commit.get("commit_hash"),
            "commit_date": commit.get("commit_date")
            or commit.get("pull_request", {}).get("mergedAt", "")[:10],
            "pull_request_text": pull_request_text,
            "change_text": change_text,
            "commit_message_text": commit.get("commit_message"),
            "filename": change_resource["filename"],
            "resource": change_resource,
        }
        return commit_info if change_text else None
