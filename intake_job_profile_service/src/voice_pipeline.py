from agents.voice import SingleAgentVoiceWorkflow, VoicePipeline
from src.voice_agent import IntakeJobProfileAgent


pipeline = VoicePipeline(workflow=SingleAgentVoiceWorkflow(IntakeJobProfileAgent().agent))