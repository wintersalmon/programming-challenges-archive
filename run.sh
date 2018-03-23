#!/bin/bash
readonly SOURCE_FILE_FORMAT="py"
readonly INPUT_FILE_FORMAT="in.txt"
readonly OUTPUT_FILE_FORMAT="out.txt"
readonly ANSWER_FILE_FORMAT="ans.txt"
readonly BASE_DIRECTORY=$(pwd)
readonly COMPARE_SCRIPT_PATH=$BASE_DIRECTORY/compare.py
readonly RE_CASE_NUMBER="s/.*\case\([!0]*[^0-9]*\)//g"
readonly RE_NUMBER='^[0-9]+$'

function echo_no_new_line() {
    echo -n $@
}

function create_file_path() {
    local path="$1/$2.$3"
    echo $path
}

function run_and_compare() {
    local target_name=$1
    local source_directory=$2
    local data_directory=$3

    local source=$(create_file_path $source_directory $target_name $SOURCE_FILE_FORMAT)
    local input=$(create_file_path $data_directory $target_name $INPUT_FILE_FORMAT)
    local output=$(create_file_path $data_directory $target_name $OUTPUT_FILE_FORMAT)
    local answer=$(create_file_path $data_directory $target_name $ANSWER_FILE_FORMAT)

    cat $input | python $source > $output

    python $COMPARE_SCRIPT_PATH $output $answer
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

case_dirs=$(find $target_directory -name '*.in.txt')
for dir in $case_dirs; do
    data_directory=$(dirname $dir)
    case_number=$(echo $data_directory | sed -e $RE_CASE_NUMBER)
    
    # case is not number
    if ! [[ $case_number =~ $RE_NUMBER ]] ; then
        case_number="'default'"
    fi

    # if not all is selected only run case matching target number
    if [ "$target_case_number" = "all" ] || [ "$target_case_number" = "$case_number" ]; then
        echo_no_new_line "- with case $case_number:"
        run_and_compare $target_name $target_directory $data_directory
        echo " done"
    fi

done

