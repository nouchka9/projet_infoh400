from app.db.repositories.patient_repository import PatientRepository
from app.db.repositories.message_repository import MessageRepository
from hl7apy.core import Message as HL7Message

def route_message(patient, message):
    """
    Dirige le message vers la bonne logique selon son type.

    Args:
        patient (Patient): Données patient
        message (Message): Message HL7 reçu

    Returns:
        str: Message ACK HL7
    """
    patient_repo = PatientRepository()
    message_repo = MessageRepository()

    # Enregistrer le message
    message_repo.save(message)

    # Enregistrer ou mettre à jour le patient
    if patient:
        patient_repo.update(patient)

    # Générer un ACK HL7
    ack = HL7Message("ACK")
    ack.msh.msh_3 = message.destination
    ack.msh.msh_5 = message.source
    ack.msh.msh_7 = message.created_at.replace("-", "").replace(":", "").split(".")[0]
    ack.msh.msh_9 = "ACK"
    ack.msh.msh_10 = message.id
    ack.msh.msh_11 = "P"
    ack.msh.msh_12 = "2.5"
    ack.msa.msa_1 = "AA"
    ack.msa.msa_2 = message.id

    return ack.to_er7()
# # Ce fichier permet d'utiliser le dossier hl7_engine comme un package Python
# # Ce fichier permet d'utiliser le dossier router comme un package Python