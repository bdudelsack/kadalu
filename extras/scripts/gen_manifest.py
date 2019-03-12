import sys

from jinja2 import Template

MANIFESTS_DIR = "manifests/"


def template(filename, template_file=None, template_args={}):
    if template_file is None:
        template_file = filename + ".j2"

    filename = MANIFESTS_DIR + filename
    template_file = MANIFESTS_DIR + template_file

    content = ""
    with open(template_file) as f:
        content = f.read()

    Template(content).stream(
        **template_args).dump(filename)


if __name__ == "__main__":
    template_args = {
        "volname": "glustervol",
        "kube_hostname": sys.argv[1],
        "namespace": "kadalu",
        "brick_path": "/data/brick",
        "host_brick_path": sys.argv[2],
        "kadalu_version": "latest",
    }

    manifest_files = [
        "00-namespace.yaml",
        "01-configmap.yaml",
        "02-server.yaml",
        "03-csi.yaml",
        "04-storageclass.yaml",
        "05-services.yaml",
        "sample-app.yaml",
        "sample-pvc.yaml"
    ]

    for filename in manifest_files:
        template(filename, template_args=template_args)
        if not filename.startswith("sample-"):
            print("kubectl create -f manifests/%s" % filename)
