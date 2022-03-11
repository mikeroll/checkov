from checkov.common.models.enums import CheckCategories, CheckResult
from checkov.terraform.checks.resource.base_resource_check import BaseResourceCheck


class PrivilegedContainersPSP(BaseResourceCheck):

    def __init__(self):
        # CIS-1.3 1.7.1
        # CIS-1.5 5.2.1
        name = "Do not admit privileged containers"
        id = "CKV_K8S_2"

        supported_resources = ['kubernetes_pod', 'kubernetes_pod_security_policy']
        categories = [CheckCategories.GENERAL_SECURITY]
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def scan_resource_conf(self, conf) -> CheckResult:
        spec = conf['spec'][0]
        if spec.get("container"):
            containers = spec.get("container")
            for idx, container in enumerate(containers):
                if container.get("security_context"):
                    context = container.get("security_context")[0]
                    if context.get("privileged") == [True]:
                        self.evaluated_keys = [f'spec/[0]/container/[{idx}]/security_context/[0]/privileged']
                        return CheckResult.FAILED
        # for psp
        if spec.get("privileged") == [True]:
            self.evaluated_keys = ['spec/[0]/privileged']
            return CheckResult.FAILED
        return CheckResult.PASSED


check = PrivilegedContainersPSP()
