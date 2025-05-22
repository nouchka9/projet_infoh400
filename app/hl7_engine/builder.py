# HL7 Message Builder
"""
Constructeur de messages HL7.
Permet de créer des messages HL7 standardisés pour différents cas d'usage hospitaliers.
"""
from hl7apy.core import Message
from datetime import datetime
import uuid
import logging

class HL7MessageBuilder:
    """Classe pour construire des messages HL7 sortants"""
    
    def __init__(self, sending_app="HL7MESSENGER", sending_facility="HOSPITAL"):
        self.logger = logging.getLogger("HL7Messenger.MessageBuilder")
        self.sending_app = sending_app
        self.sending_facility = sending_facility
    
    def _get_timestamp(self):
        return datetime.now().strftime("%Y%m%d%H%M%S")
    
    def _get_control_id(self):
        return str(uuid.uuid4())[:20]
    
    def create_adt_a01(self, patient_data, receiving_app="ADT", receiving_facility="HOSPITAL"):
        self.logger.info(f"Création d'un message ADT^A01 pour le patient {patient_data.get('id', 'INCONNU')}")
        try:
            msg = Message("ADT_A01")
            control_id = self._get_control_id()
            msg.msh.msh_3 = self.sending_app
            msg.msh.msh_4 = self.sending_facility
            msg.msh.msh_5 = receiving_app
            msg.msh.msh_6 = receiving_facility
            msg.msh.msh_7 = self._get_timestamp()
            msg.msh.msh_9 = "ADT^A01"
            msg.msh.msh_10 = control_id
            msg.msh.msh_11 = "P"
            msg.msh.msh_12 = "2.5"
            msg.evn.evn_2 = self._get_timestamp()
            msg.pid.pid_1 = "1"
            msg.pid.pid_3 = patient_data.get("id", "")
            msg.pid.pid_5 = f"{patient_data.get('last_name', '')}^{patient_data.get('first_name', '')}"
            msg.pid.pid_7 = patient_data.get("birth_date", "")
            msg.pid.pid_8 = patient_data.get("gender", "")
            msg.pv1.pv1_1 = "1"
            msg.pv1.pv1_2 = "I"
            msg.pv1.pv1_3 = f"{patient_data.get('ward', '')}^{patient_data.get('room', '')}"
            msg.pv1.pv1_44 = self._get_timestamp()
            formatted_message = msg.to_er7()
            self.logger.info(f"Message ADT^A01 créé avec ID de contrôle {control_id}")
            return formatted_message, control_id
        except Exception as e:
            self.logger.error(f"Erreur lors de la création du message ADT^A01: {str(e)}")
            raise

    def create_oru_r01(self, patient_id, results_data, receiving_app="LAB", receiving_facility="HOSPITAL"):
        self.logger.info(f"Création d'un message ORU^R01 pour le patient {patient_id}")
        try:
            msg = Message("ORU_R01")
            control_id = self._get_control_id()
            msg.msh.msh_3 = self.sending_app
            msg.msh.msh_4 = self.sending_facility
            msg.msh.msh_5 = receiving_app
            msg.msh.msh_6 = receiving_facility
            msg.msh.msh_7 = self._get_timestamp()
            msg.msh.msh_9 = "ORU^R01"
            msg.msh.msh_10 = control_id
            msg.msh.msh_11 = "P"
            msg.msh.msh_12 = "2.5"
            pid = msg.add_group("ORU_R01_PATIENT")
            pid.pid.pid_1 = "1"
            pid.pid.pid_3 = patient_id
            for result_index, result in enumerate(results_data, 1):
                observation = msg.add_group("ORU_R01_OBSERVATION")
                observation.obr.obr_1 = str(result_index)
                observation.obr.obr_2 = result.get("order_id", "")
                observation.obr.obr_3 = result.get("filler_id", "")
                observation.obr.obr_4 = result.get("test_code", "") + "^" + result.get("test_name", "")
                observation.obr.obr_7 = self._get_timestamp()
                for obx_index, test_result in enumerate(result.get("results", []), 1):
                    obx = observation.add_segment("OBX")
                    obx.obx_1 = str(obx_index)
                    obx.obx_2 = test_result.get("type", "NM")
                    obx.obx_3 = test_result.get("code", "") + "^" + test_result.get("name", "")
                    obx.obx_5 = test_result.get("value", "")
                    obx.obx_6 = test_result.get("unit", "")
                    obx.obx_7 = test_result.get("reference_range", "")
                    obx.obx_8 = test_result.get("abnormal_flag", "")
                    obx.obx_11 = "F"
                    obx.obx_14 = self._get_timestamp()
            formatted_message = msg.to_er7()
            self.logger.info(f"Message ORU^R01 créé avec ID de contrôle {control_id}")
            return formatted_message, control_id
        except Exception as e:
            self.logger.error(f"Erreur lors de la création du message ORU^R01: {str(e)}")
            raise

    def create_orm_o01(self, patient_id, order_data, receiving_app="ORDER", receiving_facility="HOSPITAL"):
        self.logger.info(f"Création d'un message ORM^O01 pour le patient {patient_id}")
        try:
            msg = Message("ORM_O01")
            control_id = self._get_control_id()
            msg.msh.msh_3 = self.sending_app
            msg.msh.msh_4 = self.sending_facility
            msg.msh.msh_5 = receiving_app
            msg.msh.msh_6 = receiving_facility
            msg.msh.msh_7 = self._get_timestamp()
            msg.msh.msh_9 = "ORM^O01"
            msg.msh.msh_10 = control_id
            msg.msh.msh_11 = "P"
            msg.msh.msh_12 = "2.5"
            patient_group = msg.add_group("ORM_O01_PATIENT")
            patient_group.pid.pid_1 = "1"
            patient_group.pid.pid_3 = patient_id
            order_group = msg.add_group("ORM_O01_ORDER")
            order_group.orc.orc_1 = "NW"
            order_group.orc.orc_2 = order_data.get("order_id", self._get_control_id())
            order_group.orc.orc_9 = self._get_timestamp()
            order_detail = order_group.add_group("ORM_O01_ORDER_DETAIL")
            order_detail.obr.obr_1 = "1"
            order_detail.obr.obr_2 = order_data.get("order_id", "")
            order_detail.obr.obr_4 = order_data.get("test_code", "") + "^" + order_data.get("test_name", "")
            order_detail.obr.obr_7 = self._get_timestamp()
            if "scheduled_date" in order_data:
                order_detail.obr.obr_36 = order_data.get("scheduled_date", "")
            if "comments" in order_data and order_data["comments"]:
                nte = order_group.add_segment("NTE")
                nte.nte_1 = "1"
                nte.nte_3 = order_data["comments"]
            formatted_message = msg.to_er7()
            self.logger.info(f"Message ORM^O01 créé avec ID de contrôle {control_id}")
            return formatted_message, control_id
        except Exception as e:
            self.logger.error(f"Erreur lors de la création du message ORM^O01: {str(e)}")
            raise
