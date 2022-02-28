import logging
import re
from onapsdk.sdc.service import Service
from onapsdk.clamp.clamp_element import Clamp
from onapsdk.clamp.loop_instance import LoopInstance
from jinja2 import Environment, FileSystemLoader, select_autoescape, ChoiceLoader
from config import Config

#Constants
VERSION = "09"
CLAMP_SUBVERSION = "down"
SERVICE_NAME = Config.SERVICENAME
POLICY_NAME = ["Drools"]
LOOP_INSTANCE_NAME = "test_ad_" + VERSION  + CLAMP_SUBVERSION

class MyLoopInstance(LoopInstance):
    jinja_env=Environment(autoescape=select_autoescape(['html', 'htm', 'xml']),
                       loader=ChoiceLoader([
                       FileSystemLoader(searchpath="./templates/")
                   ]))
    def update_microservice_policy(self) -> None:
        """
        Update microservice policy configuration.

        Update microservice policy configuration using payload data.

        """
        url = f"{self.base_url()}/loop/updateMicroservicePolicy/{self.name}"
        template = self.jinja_env.get_template("ad_clamp_add_tca_config.json.j2")
        microservice_name = self.details["globalPropertiesJson"]["dcaeDeployParameters"]\
                                        ["uniqueBlueprintParameters"]["policy_id"]
        data = template.render(name=microservice_name,
                               LOOP_name_up='test_ad_scale_up',
                               LOOP_name_down='test_ad_scale_down',
                               policyName= "DCAE.Config_tca-hi-lo",
                               controlLoopSchemaType= "VNF")

        self.send_message('POST',
                          'ADD TCA config',
                          url,
                          data=data)

    def add_drools_conf(self) -> dict:
        """Add drools configuration."""
        self.validate_details()
        vfmodule_dicts = self.details["modelService"]["resourceDetails"]["VFModule"]
        vf_dicts = self.details['modelService']['resourceDetails']['VF']
        vf_name = None
        m=re.match(r"^{'(.*)':\s{'resourceVendor'",str(vf_dicts))
        if m:
            print("group:")
            vf_name = m.group(1)
            print(m.group(1))
        else:
            print("no group")

        clamp_dicts = self.details['modelService']['resourceDetails']['VF'][vf_name]['controllerProperties']
        template = self.jinja_env.get_template("ad_clamp_add_drools_policy.json.j2")
        data = template.render(name=self.extract_operational_policy_name("Drools"),
                               artifact_name= clamp_dicts['sdnc_model_name'],
                               artifact_version= clamp_dicts['sdnc_model_version'],
                               targetType = 'VNF',
                               LOOP_name='test_ad_scale_down',
                               operation = "scale",
                               data ="{'replica-count': '1'}")
        return data



#Service already created in this case

logger = logging.getLogger("")
logger.setLevel(logging.INFO)
fh = logging.StreamHandler()
fh_formatter = logging.Formatter('%(asctime)s %(levelname)s %(lineno)d:%(filename)s(%(process)d) - %(message)s')
fh.setFormatter(fh_formatter)
logger.addHandler(fh)



logger.info("*******************************")
logger.info("******** SERVICE FETCH *******")
logger.info("*******************************")

svc = Service(name=SERVICE_NAME)
print(svc.name)
logger.info("***************************************")
logger.info("******** CLAMP AUTHENTIFICATION *******")
logger.info("***************************************")
Clamp()
logger.info("*************************************")
logger.info("******** LOOP TEMPLATES CHECK *******")
logger.info("*************************************")

loop_template = Clamp.check_loop_template(service=svc)
if not loop_template:
    logger.error("Loop template for the service %s not found", svc.name)
    exit(1)

logger.info("*******************************")
logger.info("******** POLICIES CHECK *******")
logger.info("*******************************")

drools_exists = Clamp.check_policies(policy_name=POLICY_NAME[0],
                                        req_policies=30)
policy_exists = (drools_exists)
if not policy_exists:
    logger.error("Couldn't load the policy %s", POLICY_NAME)
    exit(1)

logger.info("***********************************")
logger.info("******** LOOP INSTANTIATION *******")
logger.info("***********************************")

loop = MyLoopInstance(template=loop_template, name=LOOP_INSTANCE_NAME, details={})
loop.create()
if loop.details:
    logger.info("Loop instance %s successfully created !!", LOOP_INSTANCE_NAME)
else:
    logger.error("An error occured while creating the loop instance")

logger.info("******** UPDATE MICROSERVICE POLICY *******")
loop._update_loop_details()
loop.update_microservice_policy()

logger.info("******** ADD OPERATIONAL POLICY DROOLS *******")
added = loop.add_operational_policy(policy_type="onap.policies.controlloop.operational.common.Drools",
                                    policy_version="1.0.0")

logger.info("******** CONFIGURE OPERATIONAL POLICY DROOLS *******")
try:
    loop.add_op_policy_config(loop.add_drools_conf)
except:
    pass

logger.info("******** SUBMIT POLICIES TO PE *******")
submit = True
submit = loop.act_on_loop_policy(loop.submit)
logger.info("******** CHECK POLICIES SUBMITION *******")
if submit :
    logger.info("Policies successfully submited to PE")
else:
    logger.error("An error occured while submitting the loop instance")
    exit(1)

logger.info("******** DEPLOY LOOP INSTANCE *******")
deploy=True
deploy = loop.deploy_microservice_to_dcae()
if deploy:
    logger.info("Loop instance %s successfully deployed on DCAE !!", LOOP_INSTANCE_NAME)
else:
    logger.error("An error occured while deploying the loop instance")
    exit(2)

