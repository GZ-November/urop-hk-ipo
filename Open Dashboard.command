#!/bin/zsh
# Open the self-contained dashboard from any checkout location.
project_dir="${0:A:h}"
open "$project_dir/dashboard/index.html"
