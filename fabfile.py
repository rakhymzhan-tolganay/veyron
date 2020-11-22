from fabric.api import run, sudo, env, hosts
import os


test_manager_ip = os.getenv('TEST_ADDR')
# docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY


@hosts([test_manager_ip])
def test():
    env.hosts = [test_manager_ip]
    env.branch = os.getenv('TEST_GIT_BRANCH')
    env.app_path = os.getenv('TEST_APP_PATH')
    env.user = os.getenv('TEST_USER')
    env.password = os.getenv('TEST_PASSWORD')
    env.registry = os.getenv('CI_REGISTRY')
    env.registry_login = os.getenv('CI_REGISTRY_USER')
    env.registry_password = os.getenv('CI_REGISTRY_PASSWORD')
    env.commit_sha = os.getenv('CI_COMMIT_SHA')
    env.compose_file = 'test.yml'
    env.stack_name = os.getenv('TEST_STACK_NAME')


def make_exports():
    return 'export CI_REGISTRY=%s; ' \
           'export CI_REGISTRY_USER=%s; ' \
           'export CI_REGISTRY_PASSWORD=%s; ' \
           'export CI_COMMIT_SHA=%s' % (env.registry, env.registry_login, env.registry_password, env.commit_sha)


def git_stash():
    run('cd %s; git checkout %s; git stash' % (env.app_path, env.branch))


def git_pull():
    print('#' * 40)
    print(env.branch)
    print('#' * 40)
    run('cd %s; git fetch; git checkout %s; git pull origin %s' % (env.app_path, env.branch, env.branch))


def docker_compose_pull(exports):
    run('%s; cd %s; docker-compose -f %s pull' % (exports, env.app_path, env.compose_file))


def docker_stack_deploy(exports):
    run('%s; cd %s; docker stack deploy -c %s --with-registry-auth --prune %s' % (exports, env.app_path,
                                                                                  env.compose_file, env.stack_name))


def docker_login():
    run('docker login -u %s -p %s %s' % (env.registry_login, env.registry_password, env.registry))


def deploy():
    exports = make_exports()
    git_stash()
    git_pull()
    docker_login()
    docker_compose_pull(exports)
    docker_stack_deploy(exports)
