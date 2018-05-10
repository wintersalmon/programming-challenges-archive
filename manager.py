import difflib
import json
import os
import sys
import time

from tools.api import APIUdebug

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SRC_DIR)


def compare_file_content(ans_file_path, out_file_path):
    with open(ans_file_path, 'r') as from_file:
        with open(out_file_path, 'r') as to_file:
            return [line for line in
                    difflib.unified_diff(
                        from_file.readlines(),
                        to_file.readlines(),
                        fromfile='Answer',
                        tofile='Current',
                        lineterm='')]


def get_or_create_dir(*paths, mode=0o755):
    target_dir = os.path.join(*paths)
    if not os.path.exists(target_dir):
        cur_path = paths[0]
        for path in paths[1:]:
            cur_path = os.path.join(cur_path, path)
            if not os.path.exists(cur_path):
                os.mkdir(path=cur_path, mode=mode)

    return target_dir


def create(judge_alias, problem_id):
    api = APIUdebug.load_from_file('.secret.json')
    input_list = api.get_input_list(judge_alias, problem_id)

    conf = {
        'judge_alias': judge_alias,
        'problem_id': problem_id,
        'cases': input_list
    }

    project_root_dir = get_or_create_dir(SRC_DIR, judge_alias, problem_id)
    project_conf_file_path = os.path.join(project_root_dir, '.{}_{}.json'.format(judge_alias, problem_id))
    project_src_file_path = os.path.join(project_root_dir, '{}_{}.py'.format(judge_alias, problem_id))

    print(project_root_dir)

    with open(project_conf_file_path, 'w') as conf_file:
        json.dump(conf, conf_file)

    with open(project_src_file_path, 'w'):
        pass

    for c_num, case in enumerate(conf['cases'], 1):
        case_name = 'case_{:02d}'.format(c_num)
        case_dir = get_or_create_dir(project_root_dir, case_name)
        in_case_path = os.path.join(case_dir, '{}_{}.in.txt'.format(judge_alias, problem_id))
        ans_case_path = os.path.join(case_dir, '{}_{}.ans.txt'.format(judge_alias, problem_id))

        print(case_dir)

        in_case = api.get_input(case['id'])
        ans_case = api.get_output(case['id'])

        with open(in_case_path, 'w') as in_case_file:
            in_case_file.write(in_case)

        with open(ans_case_path, 'w') as ans_case_file:
            ans_case_file.write(ans_case)

        print('done')


def find_case_path(target_path):
    cases = list()
    for root, dirs, files in os.walk(target_path):
        for file in files:
            if file.endswith("in.txt"):
                case_path = root
                cases.append((os.path.split(root)[-1], case_path))
    return sorted(cases)


def run_all_script(judge_alias, problem_id):
    base_dir = os.path.join(SRC_DIR, judge_alias, problem_id)
    base_name = '{j_id}_{p_id}'.format(j_id=judge_alias, p_id=problem_id)

    cases = find_case_path(base_dir)
    source_file_path = os.path.join(base_dir, base_name + '.py')

    print('RUNNING {}'.format(base_name))
    for case_name, case_path in cases:
        print('- with case {}:'.format(case_name), end=' ')
        input_file_path = os.path.join(case_path, base_name + '.in.txt')
        output_file_path = os.path.join(case_path, base_name + '.out.txt')
        answer_file_path = os.path.join(case_path, base_name + '.ans.txt')

        run_counter = run_script(
            input_file_path=input_file_path, output_file_path=output_file_path, source_file_path=source_file_path)

        cmp_result = compare_file_content(ans_file_path=answer_file_path, out_file_path=output_file_path)

        if cmp_result:
            result_msg = '[{:.4f}] FAILED'.format(run_counter)
        else:
            result_msg = '[{:.4f}] OK'.format(run_counter)

        print(result_msg)
    print('DONE {}'.format(base_name))


def run_script(input_file_path, output_file_path, source_file_path):
    start = time.time()
    os.system(
        "cat {input_file_path} | python {source_file_path} > {output_file_path}".format(
            input_file_path=input_file_path, output_file_path=output_file_path, source_file_path=source_file_path))
    return time.time() - start


def main():
    command = sys.argv[1]
    judge_alias = sys.argv[2]
    problem_id = sys.argv[3]
    case_number = sys.argv[4] if len(sys.argv) == 5 else 'all'

    if command == 'run':
        run_all_script(judge_alias, problem_id)
    elif command == 'new':
        create(judge_alias, problem_id)
    else:
        print('Invalid command', command)
        exit(1)


if __name__ == '__main__':
    # create('uva', '100')
    # run('uva', '100')
    # run('test', 'echo')
    main()
