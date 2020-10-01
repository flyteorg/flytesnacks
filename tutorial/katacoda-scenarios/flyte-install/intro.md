# Flyte 

[![Current Release](https://img.shields.io/github/release/lyft/flyte.svg)](https://github.com/lyft/flyte/releases/latest)
[![Build Status](https://travis-ci.org/lyft/flyte.svg?branch=master)](https://travis-ci.org/lyft/flyte)
[![License](https://img.shields.io/badge/LICENSE-Apache2.0-ff69b4.svg)](http://www.apache.org/licenses/LICENSE-2.0.html)
![Commit activity](https://img.shields.io/github/commit-activity/w/lyft/flyte.svg?style=plastic)
![Commit since last release](https://img.shields.io/github/commits-since/lyft/flyte/latest.svg?style=plastic)
![GitHub milestones Completed](https://img.shields.io/github/milestones/closed/lyft/flyte?style=plastic)
![GitHub next milestone percentage](https://img.shields.io/github/milestones/progress-percent/lyft/flyte/8?style=plastic)
![Twitter Follow](https://img.shields.io/twitter/follow/flyteorg?label=Follow&style=social)
[![Slack Status](https://img.shields.io/badge/slack-join_chat-white.svg?logo=slack&style=social)](https://docs.google.com/forms/d/e/1FAIpQLSf8bNuyhy7rkm77cOXPHIzCm3ApfL7Tdo7NUs6Ej2NOGQ1PYw/viewform?pli=1)

Flyte is a container-native, type-safe workflow and pipelines platform optimized for large scale processing and machine learning written in Golang. Workflows can be written in any language, with out of the box support for Python. 

# Homepage
- [flyte.org](https://flyte.org)
- [Docs](https://lyft.github.io/flyte)

# Introduction
Flyte is a fabric that connects disparate computation backends using a type safe data dependency graph. It records all changes to a pipeline, making it possible to rewind time. It also stores
a history of all executions and provides an intuitive UI, CLI and REST/gRPC API to interact with the computation.

Flyte is more than a workflow engine, it provides workflows as a core concepts, but it also provides a single unit of execution - tasks, as a top level concept. Multiple tasks arranged in a data
producer-consumer order creates a workflow. Flyte workflows are pure specification and can be created using any language. Every task can also by any language. We do provide first class support for
python, making it perfect for modern Machine Learning and Data processing pipelines.

# Resources
Resources that would help you get a better understanding of Flyte.

# Communication channels
- [Slack Org](https://docs.google.com/forms/d/e/1FAIpQLSf8bNuyhy7rkm77cOXPHIzCm3ApfL7Tdo7NUs6Ej2NOGQ1PYw/viewform?pli=1)
