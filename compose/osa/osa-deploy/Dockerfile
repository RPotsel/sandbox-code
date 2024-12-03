# https://docs.openstack.org/project-deploy-guide/openstack-ansible/latest/deploymenthost.html
# https://docs.openstack.org/openstack-ansible/latest/doc-openstack-ansible.pdf
# docker build . -t openstack-ansible:2024.1
# docker run -dit --name osa-deploy openstack-ansible:2024.1
# docker exec -it osa-deploy bash
FROM alpine:3.20.3
RUN apk add --no-cache bash build-base git python3-dev openssh-client openssh-keygen sudo py3-virtualenv iptables libffi-dev openssl-dev linux-headers coreutils curl
RUN git clone -b stable/${TAG:-latest} https://opendev.org/openstack/openstack-ansible /opt/openstack-ansible
WORKDIR /opt/openstack-ansible
RUN /opt/openstack-ansible/scripts/bootstrap-ansible.sh
ENTRYPOINT ["bash"]
