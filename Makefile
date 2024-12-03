# WORKSPASE?=example
# HOST?=gitlab_docker
# CODE?=git-copy

WORKSPASE?=k8s
HOST?=k8s_worker
# CODE?=kubernetes
CODE?=DevOps
TAGS?=all

export ANSIBLE_INVENTORY_PLUGINS=~/.ansible/plugins/inventory:/usr/share/ansible/plugins/inventory:$(shell pwd)/plugins/inventory
export ANSIBLE_INVENTORY_ENABLED=host_list,script,auto,yaml,ini,libvirt_qemu
export ANSIBLE_LOCALHOST_WARNING=false
export ANSIBLE_HOST_KEY_CHECKING=false
export ANSIBLE_INVENTORY_UNPARSED_WARNING=false
export ANSIBLE_ROLES_PATH=$(shell pwd)/roles

init:
	pip3 install -r requirements.txt

compose-deploy:
	@ansible $(HOST) -m community.docker.docker_compose -i ./inventory/$(WORKSPASE) \
	--args "project_src=./compose/$(CODE) env_file=./compose/$(CODE)/.env.$(WORKSPASE)"

compose-down:
	@ansible $(HOST) -m community.docker.docker_compose -i ./inventory/$(WORKSPASE) \
	--args "project_src=./compose/$(CODE) env_file=./compose/$(CODE)/.env.$(WORKSPASE) \
			state=absent"

# FIX: The tags is not working
ans-role:
	@ansible $(HOST) -b -m ansible.builtin.include_role \
		-a '{ "name":"$(CODE)", "apply":{"tags":"$(TAGS)"} }' -i ./inventory/$(WORKSPASE)
		# --vault-password-file ./inventory/$(WORKSPASE)/.vault

ans-playbook:
	@ansible-playbook ./playbook/$(CODE)/playbook.yml -i ./inventory/$(WORKSPASE) \
		--tags $(TAGS)
		# --vault-password-file ./inventory/$(WORKSPASE)/.vault

ans-list:
	ansible-inventory -i ./inventory/$(WORKSPASE) --list
	ansible -i ./inventory/$(WORKSPASE) $(HOST) -m ansible.builtin.setup
