# !/bin/bash


function find_case_path() {
    local target_category=$1
    local target_problem=$2

    output=$(python './.tools/settings.py' $target_category $target_problem)
    result=$?

    if [ $result = 0 ]; then
        echo $output
        return 0
    else
        return $result
    fi

}

target_category=$1
target_problem=$2

result=$(find_case_path $target_category $target_problem)
if [ $? = 0 ]; then
    for path in $result; do
        echo $path
    done
fi
