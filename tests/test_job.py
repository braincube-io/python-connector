# -*- coding: utf-8 -*-
"""Tests for the memory_base module."""

from tests.mock import job_obj


def test_create_job(job_obj):
    job_obj._name == "job1"
