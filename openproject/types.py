from typing import TypedDict, List, Optional, Union
from datetime import datetime


class Link(TypedDict, total=False):
    href: str
    title: str | None
    method: str | None
    type: str | None
    payload: str | None
    templated: bool | None


class Payload(TypedDict, total=False):
    user: Link


class CustomAction(TypedDict, total=False):
    href: str
    method: str
    title: str


class Description(TypedDict, total=False):
    format: str
    raw: str
    html: str


class Links(TypedDict, total=False):
    self: Link
    schema: Link
    update: Link
    delete: Link
    log_time: Link
    move: Link
    attachments: Link
    add_attachment: Link
    author: Link
    custom_actions: List[CustomAction]
    responsible: Link
    relations: Link
    revisions: Link
    assignee: Link
    priority: Link
    project: Link
    status: Link
    type: Link
    version: Link
    available_watchers: Link
    watch: Link
    add_watcher: Link
    remove_watcher: Link
    add_relation: Link
    change_parent: Link
    add_comment: Link
    parent: Link
    category: Link
    children: List[Link]
    ancestors: List[Link]
    time_entries: Link
    watchers: Link
    custom_field_3: Link


class WorkPackage(TypedDict, total=False):
    _links: Links
    subject: str
    description: Description
    schedule_manually: bool
    readonly: bool
    start_date: datetime
    due_date: datetime
    derived_start_date: datetime
    derived_due_date: datetime
    estimated_time: str
    derived_estimated_time: str
    percentage_done: int
    custom_field_1: str
    custom_field_2: int
    created_at: str
    updated_at: str


class StatusExplanation(TypedDict, total=False):
    format: str
    raw: str
    html: str


class Project(TypedDict, total=False):
    _links: Links
    name: str
    status_explanation: StatusExplanation
    description: Description
