from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from dotenv import load_dotenv
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, FileWriterTool

load_dotenv()

@CrewBase
class AiNews():
	"""AiNews crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

# Agents -

	@agent
	def retrieve_news(self) -> Agent:
		return Agent(
			config=self.agents_config['retrieve_news'],
			tools=[SerperDevTool()],
			verbose=True
		)

	@agent
	def website_scraper(self) -> Agent:
		return Agent(
			config=self.agents_config['website_scraper'],
			tools=[ScrapeWebsiteTool()],
			verbose=True
		)
	
	@agent
	def ai_news_writer(self) -> Agent:
		return Agent(
			config=self.agents_config['ai_news_writer'],
			verbose=True
		)
	
	@agent
	def file_writer(self) -> Agent:
		return Agent(
			config=self.agents_config['file_writer'],
			tools=[FileWriterTool()],
			verbose=True
		)
	
	# Tasks -

	@task
	def retrieve_news_task(self) -> Task:
		return Task(
			config=self.tasks_config['retrieve_news_task']
		)

	@task
	def scrape_website_task(self) -> Task:
		return Task(
			config=self.tasks_config['scrape_website_task']
		)

	@task
	def ai_news_writer_task(self) -> Task:
		return Task(
			config=self.tasks_config['ai_news_writer_task']
		)

	@task
	def file_writer_task(self) -> Task:
		return Task(
			config=self.tasks_config['file_writer_task']
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the AiNews crew"""
		return Crew(
			agents=self.agents,
			tasks=self.tasks,
			process=Process.sequential,
			verbose=True,
		)
