#!/bin/bash
readonly SOURCE_FILE_FORMAT="py"
readonly INPUT_FILE_FORMAT="in.txt"
readonly OUTPUT_FILE_FORMAT="out.txt"
readonly ANSWER_FILE_FORMAT="ans.txt"
readonly BASE_DIRECTORY=$(pwd)
readonly TOOLS_DIRECTORY=$BASE_DIRECTORY/.tools
readonly COMPARE_SCRIPT_PATH=$TOOLS_DIRECTORY/compare.py
readonly RE_CASE_NUMBER="s/.*\case\([!0]*[^0-9]*\)//g"
readonly RE_NUMBER='^[0-9]+$'

function echo_no_new_line() {
    echo -n $@
}

function create_file_path() {
    local path="$1/$2.$3"
    echo $path
}

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

function run_and_compare() {
    local target_name=$1
    local source_directory=$2
    local data_directory=$3
    if [ "$#" = 4 ]; then
        local show_result=$4
    else
        local show_result=""
    fi

    local source=$(create_file_path $source_directory $target_name $SOURCE_FILE_FORMAT)
    local input=$(create_file_path $data_directory $target_name $INPUT_FILE_FORMAT)
    local output=$(create_file_path $data_directory $target_name $OUTPUT_FILE_FORMAT)
    local answer=$(create_file_path $data_directory $target_name $ANSWER_FILE_FORMAT)

    start=`gdate +%s.%4N`
    # start=`date +%s.%4N`
    # start=$(python -c 'import time; print(time.time())')

    cat $input | python $source > $output

    end=`gdate +%s.%4N`
    # end=`date +%s.%4N`
    # end=$(python -c 'import time; print(time.time())')

    runtime=$(echo "$end-$start" | bc)

    output=$(python $COMPARE_SCRIPT_PATH $output $answer)
    compare_result=$?
    if [ $compare_result = 0 ]; then
        echo " [$runtime] OK"
    else
        echo " [$runtime] FAILED"
        if [[ $output ]] && [ $show_result ]; then
            echo "$output"
        fi
    fi
}

if [ "$#" = 2 ]; then
    target_case_number='all'

elif [ "$#" = 3 ]; then
    target_case_number=$3
 
else
    echo 'invalid params'
    exit

fi

target_category=$1
target_subcategory=$2
target_directory="$BASE_DIRECTORY/$target_category/$target_subcategory"
target_name="$target_category"_"$target_subcategory"

echo "RUNNING $target_name"
case_dirs=$(find $target_directory -name '*in.txt' | sort)
for dir in $case_dirs; do
    data_directory=$(dirname $dir)
    case_number=$(echo $data_directory | sed -e "s/.*\(case_*\)//g")

    # case is empty == default case
    if ! [[ $case_number ]] ; then
        case_number="default"
    fi

    # if not all is selected only run case matching target number
    if [ "$target_case_number" = "all" ]; then
        echo_no_new_line "- with case $case_number:"
        run_and_compare $target_name $target_directory $data_directory
    elif [ "$target_case_number" = "$case_number" ]; then
        echo_no_new_line "- with case $case_number:"
        run_and_compare $target_name $target_directory $data_directory show
    fi

done

echo "DONE $target_name"
