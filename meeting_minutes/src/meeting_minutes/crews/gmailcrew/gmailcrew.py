from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from .tools.gmail_tool import GmailTool

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class GmailCrew():
	"""Gmailcrew crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	llm = LLM(
        model="claude-3-sonnet-20240229"
    )

	@agent
	def gmail_draft_writer(self) -> Agent:
		return Agent(
			config=self.agents_config['gmail_draft_writer'],
			tools=[GmailTool()],
			verbose=True,
			llm=self.llm
		)

	@task
	def gmail_draft_task(self) -> Task:
		return Task(
			config=self.tasks_config['gmail_draft_task'],
		)


	@crew
	def crew(self) -> Crew:
		"""Creates the Gmailcrew crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
