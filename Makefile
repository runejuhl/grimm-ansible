template_id = 17

.PHONY: all
all: update launch

.PHONY: update
update:
	./bin/update-project.sh

.PHONY: launch
launch:
	./bin/launch-template.sh $(template_id)

.PHONY: build-ee
build-ee:
	ansible-builder build --tag git.petardo.dk/runejuhl/grimm-ansible/ee-ess-rocky10:latest -f ./ansible_environments/ee.yaml -v3
