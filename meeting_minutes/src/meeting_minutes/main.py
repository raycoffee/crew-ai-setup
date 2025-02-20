#!/usr/bin/env python
from pydantic import BaseModel
from crewai.flow import Flow, listen, start
from faster_whisper import WhisperModel
from crews.meeting_minutes_crew.meeting_minutes_crew import MeetingMinutesCrew
from crews.gmailcrew.gmailcrew import GmailCrew
import os
import agentops
from pathlib import Path


class MeetingMinutesState(BaseModel):
    transcript: str = ""
    meeting_minutes: str = ""   
    gmail_draft: str = ""

class MeetingMinutesFlow(Flow[MeetingMinutesState]):

    @start()
    def transcribe_meeting(self):
        print("Generating transcription")

        SCRIPT_DIR = Path(__file__).parent
        AUDIO_FILE_PATH = SCRIPT_DIR / "EarningsCall.wav"

        print(f"Transcribing {AUDIO_FILE_PATH}")

        model = WhisperModel("tiny", device="cpu")
        segments, _ = model.transcribe(str(AUDIO_FILE_PATH), beam_size=5)
        
        transcript_parts = []
        for segment in segments:
            transcript_parts.append(segment.text)
        
        self.state.transcript = " ".join(transcript_parts)
        print(f"Transcript: {self.state.transcript}")


    @listen(transcribe_meeting)
    def generate_meeting_minutes(self):
        print("Generating meeting minutes")
        inputs = {"transcript": self.state.transcript}
        
        meeting_minutes = MeetingMinutesCrew().crew().kickoff(inputs=inputs)
        
        self.state.meeting_minutes = str(meeting_minutes)



    @listen(generate_meeting_minutes)
    def create_draft_meeting_minutes(self):

        inputs = {"body": self.state.meeting_minutes}
        gmail_draft = GmailCrew().crew().kickoff(inputs=inputs)
        self.state.gmail_draft = gmail_draft


def kickoff():
    session = agentops.init(api_key=os.getenv("AGENTOPS_API_KEY"))
    meeting_minutes_flow = MeetingMinutesFlow()
    meeting_minutes_flow.plot()
    meeting_minutes_flow.kickoff()


if __name__ == "__main__":
    kickoff()
