---
layout: post
title: Measuring Coverage with XcodeCoverage, xctool, & Make
tags:
- objective-c
- xcode
- xcodecoverage
- xctool
- make
- coverage
- unit-tests
- testing
---

## The Pieces

### XcodeCoverage

The XodeCoverage [project](https://github.com/jonreid/XcodeCoverage) is a set of shell scripts bundled with `lcov` to measure lines of code coverage during execution of instrumented test builds.

In this example, the scripts are used to generate an HTML coverage report (with a few modifications made in [my fork](https://github.com/jacebrowning/XcodeCoverage/releases/tag/blog-2015-03-23) to customize report location).

### xctool

[Facebook](https://github.com/facebook/xctool) created the `xctool` command-line program to provide an easier way to build and test Xcode projects.

In this example, the tool is used to build and run Objective-C unit tests from the command line.

### Make

[Make](https://www.gnu.org/software/make/) is usually my default entry point for creating builds, running tests, and generating reports. I like putting this sort of automation in a `Makefile` because, for basic tasks, the syntax is fairly minimal and `make` is ubiquitous on most platforms.

## Putting Them Together

### The Makefile

First, we define few shared variables that can be common to all projects:

```makefile
WORKSPACE_NAME:=<???>
PROJECT_NAME:=<???>
SOURCE_NAME:=<???>
APP_NAME:=<???>

# Common
ROOT_DIR:=.
PROJECT_DIR:=$(ROOT_DIR)/$(SOURCE_NAME)
SOURCE_DIR:=$(PROJECT_DIR)/$(SOURCE_NAME)
SOURCES:=Makefile $(SOURCE_DIR)/*

# Xcode
XCODE_SCHEME?=$(APP_NAME)
XCODE_CONFIGURATION?=Debug

# xctool
XCTOOL:=xctool
XCTOOL_RESULTS_REPORTER?=pretty
XCTOOL_ARGS_SHARED:=-scheme $(XCODE_SCHEME) -configuration \
    $(XCODE_CONFIGURATION) -reporter user-notifications
XCTOOL_ARGS_TEST:=-reporter $(XCTOOL_RESULTS_REPORTER)

# XcodeCoverage
XCODECOVERAGE_DIR:=$(PROJECT_DIR)/XcodeCoverage
XCODECOVERAGE_GETCOV:=$(XCODECOVERAGE_DIR)/getcov
XCODECOVERAGE_CLEANCOV:=$(XCODECOVERAGE_DIR)/cleancov
```

and a few more variables dictating where we'd like coverage output to go:

```makefile
COVERAGE_DIR:=$(ROOT_DIR)/coverage
COVERAGE_LOG:=$(COVERAGE_DIR)/getcov.log
COVERAGE_REPORT:=$(COVERAGE_DIR)/index.html
```

The test target is defined as:

```makefile
.PHONY: test
test: $(COVERAGE_LOG)
$(COVERAGE_LOG): $(SOURCES)
    $(XCODECOVERAGE_CLEANCOV)
    $(XCTOOL) test $(XCTOOL_ARGS_SHARED) $(XCTOOL_ARGS_TEST)
    mkdir -p $(COVERAGE_DIR) && \
        $(XCODECOVERAGE_GETCOV) $(PROJECT_NAME) $(COVERAGE_DIR) > \
            $(COVERAGE_LOG)
    tail -n 3 $(COVERAGE_LOG)
```

which will:

1. Delete the old coverage data
2. Build and run the unit tests
3. Parse the generated coverage data
4. Generate an HTML coverage report
5. Display the percentage of lines coverage

A shortcut to open the coverage report is defined as:

```makefile
.PHONY: read-cov
read-cov: $(COVERAGE_INDEX)
    open $(COVERAGE_INDEX)

$(COVERAGE_INDEX): $(COVERAGE_LOG)
```

### Example Output

Running `$ make test` displays something like:

```
./MyProject/XcodeCoverage/cleancov
Deleting all .da files in /Users/Browning/Library/Developer/Xcode/DerivedData/MyWorkspace/Build/Intermediates/MyProject.build/Debug-iphonesimulator/MyProject.build/Objects-normal/x86_64 and subdirectories
Done.

xctool test -scheme MyProject -configuration Debug -reporter user-notifications -reporter pretty
[Info] Loading settings for scheme 'MyProject' ... (1950 ms)

=== TEST ===

  xcodebuild build build
    MyProject / MyProject (Debug)
      ✓ Check dependencies (111 ms)
      ✓ Write auxiliary files (0 ms)
      ✓ Compile BatterySensor.m (574 ms)
      ...
      ✓ Compile Platform.m (68 ms)
      0 errored, 0 warning (1315 ms)

  [Info] Collecting info for testables... (1196 ms)
  run-test MyProjectTests.xctest (iphonesimulator8.2, iPad Air, application-test)
    [Info] Installed 'MyProject'. (1392 ms)
    [Info] Launching test host and running tests ... (0 ms)
    ✓ -[BatterySensorCellTestCase testSensorLevel] (5 ms)
    ...
    ✓ -[GroupManagerTestCase testCanCreateGroup] (0 ms)
    99 passed, 0 failed, 0 errored, 99 total (9999 ms)

** TEST SUCCEEDED: 99 passed, 0 failed, 0 errored, 99 total ** (99999 ms)

mkdir -p ./coverage && ./MyProject/XcodeCoverage/getcov MyProject ./coverage > ./coverage/getcov.log

tail -n 3 ./coverage/getcov.log
Overall coverage rate:
  lines......: 17.6% (3676 of 20867 lines)
  functions..: 19.5% (817 of 4192 functions)

```

Running `$ make read-cov` launches a report similar to:

![sample-lcov-html-report]({{ site.assets }}/sample-lcov-html-report.png "Sample LCOV HTML Report")


