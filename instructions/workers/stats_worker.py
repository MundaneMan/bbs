#!/usr/bin/env python
# -*- coding: utf-8 -*-

import instructions.models.stats_model as stats_model


def stats_targets():
    target_stats = dict()
    # count = target_model.list_fp_targets_by_cond({"status": "normal"}, _is_count=True)
    # target_stats["target_count"] = count
    return target_stats


def stats_targets_family():
    target_family_stats = dict()
    # count = target_model.distinct_target_field_count("family_id", _is_count=True)
    # target_family_stats["target_family_count"] = count
    return target_family_stats


def do_stats_work():
    stats_result_obj = dict()
    stats_result_obj.update(stats_targets())
    stats_result_obj.update(stats_targets_family())
    stats_model.insert_stats(stats_result_obj)


def main():
    do_stats_work()

if __name__ == "__main__":
    main()

