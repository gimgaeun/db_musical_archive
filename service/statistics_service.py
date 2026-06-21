class StatisticsService:
    def __init__(self, statistics_repository):
        self.statistics_repository = statistics_repository

    def get_total_view_count(self):

        return self.statistics_repository.total_view_count()

    def get_total_spent(self):

        return self.statistics_repository.total_spent()

    def get_performance_ranking(self):

        return self.statistics_repository.performance_ranking()

    def get_actor_ranking(self):
        return self.statistics_repository.actor_ranking()
