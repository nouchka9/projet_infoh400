from hl7apy.core import Message

def build_ack(original_msg, ack_code="AA", text_message="Message reçu avec succès"):
    ack = Message("ACK")
    ack.msh.msh_3 = original_msg.msh.msh_5.value
    ack.msh.msh_4 = original_msg.msh.msh_6.value
    ack.msh.msh_5 = original_msg.msh.msh_3.value
    ack.msh.msh_6 = original_msg.msh.msh_4.value
    ack.msh.msh_7 = original_msg.msh.msh_7.value
    ack.msh.msh_9 = "ACK"
    ack.msh.msh_10 = original_msg.msh.msh_10.value
    ack.msh.msh_11 = "P"
    ack.msh.msh_12 = "2.5"
    ack.msa.msa_1 = ack_code
    ack.msa.msa_2 = original_msg.msh.msh_10.value
    ack.msa.msa_3 = text_message
    return ack.to_er7()
