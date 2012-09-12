import virtualenv, textwrap
output = virtualenv.create_bootstrap_script(textwrap.dedent("""
def after_install(options, home_dir):
    subprocess.call([join(home_dir, 'bin', 'pip'), 'install', 'django==1.4'])
    subprocess.call([join(home_dir, 'bin', 'pip'), 'install', 'pyserial'])
    subprocess.call([join(home_dir, 'bin', 'pip'), 'install', 'beautifulsoup4'])
"""))
print output
