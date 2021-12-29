from jinja2 import Environment, FileSystemLoader
import yaml

if __name__ == '__main__':
    env = Environment(loader=FileSystemLoader('.'), trim_blocks=True, lstrip_blocks=True)
    template = env.get_template('switch_template_jinja2.txt')

    with open('R1_config_params.yaml') as f:
        r1_params = yaml.safe_load(f)

    sso_models = ['9300', '9200', '3850', '3650', '2960']
    if str(r1_params['switch_model']) in sso_models:
        r1_params['redundancy'] = 'sso'

    r1_config = template.render(r1_params)
    print(r1_config)