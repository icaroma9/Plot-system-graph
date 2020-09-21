# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 15:08:53 2020

@author: icaromarley5

"""

import os
import subprocess
import sys

target_dir = "."
if "-t" in sys.argv:
    target_dir = sys.argv[sys.argv.index("-t") + 1]


remove_strings = [
    "test",
    "apps",
    "admin",
    "urls",
    "settings",
    "migrations",
]
if "-r" in sys.argv:
    remove_strings = sys.argv[sys.argv.index("-r") + 1].split(",")


extra_format = "shape=circle, style=filled"


def run_pyreverse():
    with open(os.devnull, "w") as DEV_NULL:
        subprocess.check_call(["pyreverse", "."], stdout=DEV_NULL)
        os.remove("classes.dot")
    return "packages.dot"


def plot_graph(file):
    with open(os.devnull, "w") as DEV_NULL:
        subprocess.check_call(
            [
                "sfdp",
                "-Goverlap=scale",
                file,
                "-T",
                "png",
                "-o",
                "packages.png",
            ],
            stdout=DEV_NULL,
        )
    return "packages.dot"


def clean_defined_strings(string):
    node_list = []

    node_list = collect_strings_nodes(string, remove_strings)

    return remove_nodes(string, node_list)


def remove_nodes(string, nodes):
    # remove collected nodes
    for node in nodes:
        dot_list = []
        for line in string.split("\n"):
            if f'"{node}"' not in line:
                dot_list.append(line)
        string = "\n".join(dot_list)
    return string


def open_graph(file):
    with open(file, "r") as f:
        data = f.read()
    return data


def clean_unrelated_vertices(string):
    # locates empty nodes by name
    node_list = []
    string_list = []
    for line in string.split("\n"):
        if "->" in line or not line or line[0] != '"':
            continue
        node = line.split('"')[1]
        if string.count(f'"{node}"') < 2:
            name = line.split('"')[3]
            string_list.append(name)

    node_list = collect_strings_nodes(string, string_list, contains=False)

    return remove_nodes(string, node_list)


def collect_strings_nodes(string, string_list, contains=True):
    # collect nodes ids and remove strings
    node_list = []
    for node in string_list:
        dot_list = []
        for line in string.split("\n"):
            if not contains:
                check = f'"{node}"' in line
            else:
                check = f"{node}" in line
            if check:
                node_list.append(line.split('"')[1])
            dot_list.append(line)
        string = "\n".join(string)
    return node_list


def paint_package_vertices(string):
    # add colors to apps
    colors = [
        "black",
        "blue",
        "brown",
        "crimson",
        "cyan",
        "violet",
        "green",
        "orange",
        "yellow",
        "red",
        "gray",
        "magenta",
        "pink",
        "purple",
        "salmon",
        "navy",
        "indigo",
        "gold",
        "tomato",
        "peru",
        "turquoise",
        "olive",
        "orangered",
        "coral",
        "aqua",
        "aquamarine",
        "lime",
        "midnightblue",
        "orchid",
        "royalblue",
    ]

    name = ""
    i = 0
    dot_list = []
    for line in string.split("\n"):
        if "label" in line:
            new_name = line.split('"')[3]
            if "." in new_name:
                new_name = new_name.split(".")[0]
            if new_name != name:
                name = new_name
                i += 1
            line_parts = line.split("]")
            fillcolor = colors[i]
            line_parts[0] += f",fillcolor={fillcolor}, {extra_format}"
            line = "]".join(line_parts)
        dot_list.append(line)
    string = "\n".join(dot_list)
    return string


def save_graph(string):
    with open("packages.dot", "w") as f:
        f.writelines(string)
    return "packages.dot"


def clean_package_redundancies(string):
    package_dict = {}
    for line in string.split("\n"):
        if "label" in line:
            name = line.split('"')[3]
            if "." in name:
                name = name.split(".")[0]
            node = line.split('"')[1]
            package_dict[node] = name
        elif "->" in line:
            break

    node_list = []
    for node in package_dict:
        for line in string.split("\n"):
            if "->" in line and f'"{node}"' in line:
                node_1 = line.split('"')[1]
                node_2 = line.split('"')[3]
                if package_dict[node_1] != package_dict[node_2]:
                    break
        else:
            node_list.append(node)

    return remove_nodes(string, node_list)


class ChangeDir:
    def __init__(self, newPath):
        self.newPath = newPath

    def __enter__(self):
        self.oldPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.oldPath)


if __name__ == "__main__":
    with ChangeDir(target_dir):
        delete_init = False
        if "__init__.py" not in os.listdir():
            delete_init = True
        open("__init__.py", "a").close()

        dot_file = run_pyreverse()
        dot_str = open_graph(dot_file)
        dot_str = clean_defined_strings(dot_str)
        dot_str = clean_package_redundancies(dot_str)
        dot_str = clean_unrelated_vertices(dot_str)
        dot_str = paint_package_vertices(dot_str)
        dot_file = save_graph(dot_str)
        plot_graph(dot_file)

        os.remove(dot_file)
        if delete_init:
            os.remove("__init__.py")
