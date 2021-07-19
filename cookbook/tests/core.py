TEST_MANIFEST = {
    "core.flyte_basics.lp.my_wf": {
        "type": "lp",
        "priority": "P0",
        "data": {
            "input": {"val": 25},
            "output": {
                 "o0": 625
            },
            "n0": {
                "output": {
                    "o0": 625
                },
                "input": {"val": 25},
            }
        },
        "exitCondition": {"exit_success": False, "exit_message": ""},
    },
    "core.flyte_basics.lp.go_greet": {
        "type": "lp",
        "priority": "P0",
        "data": {
            "input": {"day_of_week": "sunday", "number": 1, "am": False},
            "output": {
                 "o0": "Have a great sunday evening!",
            },
            "n0": {
                "input": {"day_of_week": "sunday", "number": 1, "am": False},
                "output": {
                    "o0": "Have a great sunday evening!",
                },
            }
        },
        "exitCondition": {"exit_success": False, "exit_message": ""},
    },
    "core.flyte_basics.hello_world.my_wf": {
        "type": "lp",
        "priority": "P0",
        "data": {
            "input": {},
            "output": {
                 "o0": "hello world",
            },
            "n0": {
                "output": {
                    "o0": "hello world"
                },
                "input": {},
            }
        },
        "exitCondition": {"exit_success": False, "exit_message": ""},
    },
    "core.flyte_basics.files.rotate_one_workflow": {
        "type": "lp",
        "priority": "P0",
        "data": {
            "input": {
                "in_image": "https://docs.python.org/3/_static/py.png",
            },
            "output": {
                "o0": {
                    "type": "single",
                },
            },
            "n0": {
                "input": {
                    "image_location": "https://docs.python.org/3/_static/py.png",
                },
                "output": {
                    "o0": {
                        "type": "single",
                    },
                },
            }
        },
        "exitCondition": {"exit_success": False, "exit_message": ""},
    },
    "core.flyte_basics.folders.download_and_rotate": {
        "type": "lp",
        "priority": "P0",
        "data": {
            "input": {
            },
            "output": {
                "o0": {
                    "type": "single",
                },
            },
            "n0": {
                "input": {
                },
                "output": {
                    "o0": {
                        "type": "multi-part",
                    },
                },
            },
            "n1": {
                "input": {
                    "img_dir": {
                        "type": "multi-part"
                    }
                },
                "output": {
                    "o0": {
                        "type": "multi-part",
                    },
                },
            }
        },
        "exitCondition": {"exit_success": False, "exit_message": ""},
    },
    "core.flyte_basics.named_outputs.my_wf": {
        "type": "lp",
        "priority": "P0",
        "data": {
            "input": {},
            "output": {
                "greet1": "hello world",
                "greet2": "hello world"
            },
            "n0": {
                "input": {},
                "output": {
                    "greet": "hello world"
                },
            },
            "n1": {
                "input": {},
                "output": {
                    "greet": "hello world"
                },
            }
        },
        "exitCondition": {"exit_success": False, "exit_message": ""},
    },
    "core.flyte_basics.basic_workflow.my_wf": {
        "type": "lp",
        "priority": "P0",
        "data": {
            "input": {
                "a": 5,
                "b": "world"
            },
            "output": {
                "o0": 7,
                "o1": "worldworld"
            },
            "n0": {
                "input": {
                    "a": 5,
                },
                "output": {
                    "c": "world",
                    "t1_int_output": 7
                },
            },
            "n1": {
                "input": {
                    "a": "world",
                    "b": "world"
                },
                "output": {
                    "o0": "worldworld"
                },
            }
        },
        "exitCondition": {"exit_success": False, "exit_message": ""},
    },
    "core.flyte_basics.lp.square": {
        "type": "task",
        "priority": "P0",
        "data": {
            "input": {"val": 5},
            "output": {
                "o0": 25
            },
            "n0": {
                "input": {"val": 5},
                "output": {
                    "o0": 25
                },
            }
        },
        "exitCondition": {"exit_success": False, "exit_message": ""},
    },
    "core.flyte_basics.lp.greet": {
        "type": "task",
        "priority": "P0",
        "data": {
            "input": {"day_of_week": "sunday", "number": 1, "am": False},
            "output": {
                "o0": "Have a great sunday evening!"
            },
            "n0": {
                "input": {"day_of_week": "sunday", "number": 1, "am": False},
                "output": {
                    "o0": "Have a great sunday evening!"
                },
            }
        },
        "exitCondition": {"exit_success": False, "exit_message": ""},
    }
}
