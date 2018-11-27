
import json
import os
import argparse


if __name__=='__main__':



    parser = argparse.ArgumentParser()

    parser.add_argument('-template_file', action='store',
                        dest='template',
                        help='template file  with file structure', type=str, default='template.json')

    parser.add_argument('-dir', action='store',
                        dest='directory',
                        help=' where create the structure', type=str, required=True)

    parser.add_argument('-hiddenfile', action='store',
                        dest='hiddenfile',
                        help='if you want to have hidden file to save folder in git', type=bool, default=True)


    args = parser.parse_args()

    template_file = args.template
    directory= args.directory
    hidden=args.hiddenfile

    with open(template_file) as f:
        data = json.load(f)

    for main_directory in data['main_directories']:
        if "@" in main_directory:
            main_directory = main_directory.split('@')[1]
            os.mkdir(os.path.join(directory,main_directory))
            open(os.path.join(directory,main_directory,'__init__.py'), 'w').close()
        else:
            os.mkdir(os.path.join(directory, main_directory))
        if hidden:
            open(os.path.join(directory, main_directory, '.4git'), 'w').close()


    for sub_directory in data['sub_directories']:
        father = sub_directory['father']
        for dir in sub_directory['dirs']:
            if '*' in dir:
                suffix,num = dir.split('*')
                l_dir = []
                for n in range(0, int(data[num]), 1):
                    l_dir.append(data[suffix]+str(n))
                for item in l_dir:
                    os.mkdir(os.path.join(directory,father,item))
                    if hidden:
                        open(os.path.join(directory,father,item,'.4git'), 'w').close()

            else:
                os.mkdir(os.path.join(directory,father,dir))
                if hidden:
                    open(os.path.join(directory, father, item, '.4git'), 'w').close()




