from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import FileWriterTool
from dotenv import load_dotenv
import time
import os

load_dotenv()

@CrewBase
class MeetingMinutesCrew():
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # llm = LLM(
    #     model="ollama/llama3.2",
    #     base_url="http://localhost:11434"
    # )
    llm = LLM(
        model="claude-3-sonnet-20240229",
        request_timeout=60,
        max_retries=5,
        temperature=0.7,
    )

    def __init__(self):
        self.file_writer_tools = {
            'summary': FileWriterTool(
                name="Summary Writer Tool",
                dir="meeting_minutes",
                file_name="summary.txt",
                description="Write the meeting summary to a file"
            ),
            'action_items': FileWriterTool(
                name="Action Items Writer Tool",
                dir="meeting_minutes",
                file_name="action_items.txt",
                description="Write the action items to a file"
            ),
            'sentiment': FileWriterTool(
                name="Sentiment Writer Tool",
                dir="meeting_minutes",
                file_name="sentiment.txt",
                description="Write the sentiment analysis to a file"
            )
        }


    @agent
    def meeting_minutes_summarizer(self) -> Agent:
        return Agent(
            config=self.agents_config["meeting_minutes_summarizer"],
            tools=list(self.file_writer_tools.values()),
            verbose=True,
            llm=self.llm
        )
    
    @agent
    def meeting_minutes_writer(self) -> Agent:
        return Agent(
            config=self.agents_config["meeting_minutes_writer"],
            llm=self.llm
        )
    


    @task
    def meeting_minutes_summary_task(self) -> Task:
        return Task(
            config=self.tasks_config["meeting_minutes_summary_task"],
        )
    
    @task
    def meeting_minutes_writing_task(self) -> Task:
        return Task(
            config=self.tasks_config["meeting_minutes_writing_task"],
        )
    

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            max_rpm=4
        )

    def kickoff(self, inputs=None):
        return super().kickoff(inputs)
