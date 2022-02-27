# ============LICENSE_START=======================================================
# Copyright (C) 2021 Orange
# ================================================================================
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# ============LICENSE_END=========================================================

class Config:
    K8S_NAMESPACE = "test-cnf"
    K8S_VERSION = "1.18.9"
    K8S_REGION = "cnf-region"

    #### SERVICE DETAILS ####
    NATIVE = True
    SKIP_POST_INSTANTIATION = True
    MACRO_INSTANTIATION = True  # A-la-carte instantiation if False
    GLOBAL_CUSTOMER_ID = "customer_cnf"
    VSPFILE = "vsp/native_cnf_k8s_demo.zip"

    ARTIFACT_FILE ="vsp/k8s-tcagen2-clampnode-master.yaml"
    ARTIFACT_NAME = "clampnode"
    ARTIFACT_TYPE = "DCAE_INVENTORY_BLUEPRINT"
    
    PROFILE_NAME = "node-port-profile"
    PROFILE_SOURCE = PROFILE_NAME
    RELEASE_NAME = "rel-1"

    VENDOR = "vendor_cnf"
    SERVICENAME = "apache_k8s_demo_CNF"
    VSPNAME = "VSP_" + SERVICENAME
    VFNAME = "VF_" + SERVICENAME
    SERVICE_INSTANCE_NAME = "INSTANCE_" + SERVICENAME
    SDNC_ARTIFACT_NAME = "vnf"
    ADD_PNF = False

    # INSERT PARAMS FOR VNF HERE AS "name" : "value" PAIR
    VNF_PARAM_LIST = {
        "k8s-rb-profile-namespace": K8S_NAMESPACE,
        "k8s-rb-profile-k8s-version": K8S_VERSION
    }

    VF_MODULE_PREFIX = "helm_"

    VF_MODULE_PARAM_LIST = {
        VF_MODULE_PREFIX + "apache": {
            "instantiation_parameters": {
                "k8s-rb-profile-name": PROFILE_NAME,
                "k8s-rb-profile-source": PROFILE_SOURCE,
                "k8s-rb-instance-release-name": RELEASE_NAME + "-apache",
                "k8s-rb-profile-namespace": K8S_NAMESPACE,
                "k8s-rb-config-template-name": "replica-count-template",
                "k8s-rb-config-template-source": "deployment-config",
                "k8s-rb-config-name": "replica-count-change",
                "k8s-rb-config-value-source": "custom-values"
            },
            "cloud_configuration": K8S_REGION
        }
    }
    ######## DEFAULT VALUES ########
    OWNING_ENTITY = "OE-Demonstration"
    PROJECT = "Project-Demonstration"
    PLATFORM = "test"
    LINE_OF_BUSINESS = "LOB-Demonstration"

    #### REGION DETAILS ####
    CLOUD_REGIONS = {
        K8S_REGION: {
            "complex_id": "k8s-complex1",
            "cloud_owner": "K8sCloudOwner",
            "cloud_type": "k8s",
            "availability_zone": "k8s-availability-zone",
            "tenant": {
                "name": K8S_REGION + "-tenant"
            },
            "customer_resource_definitions": [
                # Uncomment lines below, if you want to run on non KUD k8s cluster
                # "crds/crd1",
                # "crds/crd2"
            ],
            "cluster_kubeconfig_file": "artifacts/kubeconfig"
        # },
        # "openstack-region-test-1": {
        #     "complex_id": "complex1",
        #     "cloud_owner": "CloudOwner",
        #     "cloud_type": "openstack",
        #     "availability_zone": "Main",
        #     "identity_url": "http://test:5000/v4",
        #     "mso_id": "test_use",
        #     "mso_pass": "test_password",
        #     "identity_server_type": "KEYSTONE_V3",
        #     "tenant": {
        #         "id": "5117085204e84027a8d1a0cf34abb0ba",
        #         "name": "onap-dev"
        #     }
        }
    }
