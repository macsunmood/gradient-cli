"""
Dupa Jasia
"""
from gradient.config import config
from .base_client import BaseClient
from ..clients import http_client
from ..models import Job
from ..serializers import JobSchema
from ..repositories.jobs import ListJobs, ListJobLogs, ListJobArtifacts
from ..utils import MessageExtractor


class JobsClient(BaseClient):
    """
    Cycki Toma
    """

    def create(
            self,
            machine_type,
            container,
            project_id,
            data,
            name=None,
            command=None,
            ports=None,
            is_public=None,
            workspace=None,
            workspace_archive=None,
            workspace_url=None,
            working_directory=None,
            ignore_files=None,
            experiment_id=None,
            job_env=None,
            use_dockerfile=None,
            is_preemptible=None,
            project=None,
            started_by_user_id=None,
            rel_dockerfile_path=None,
            registry_username=None,
            registry_password=None,
            cluster=None,
            cluster_id=None,
            node_attrs=None,
    ):
        """
        Method to create job in paperspace gradient.

        :param str machine_type: Type of machine on which job should run. This field is **required**.

            Choose one of this:

            .. code-block::

                K80
                P100
                TPU
                GV100
                GV100x8
                G1
                G6
                G12

        :param str container: name of docker container that should be used to run job. This field is **required**.

            Example value: ``tensorflow/tensorflow:1.13.1-gpu-py3``
        :param str project_id:
        :param data:
        :param name:
        :param command:
        :param ports:
        :param is_public:
        :param workspace:
        :param workspace_archive:
        :param workspace_url:
        :param working_directory:
        :param ignore_files:
        :param experiment_id:
        :param job_env:
        :param use_dockerfile:
        :param is_preemptible:
        :param project:
        :param started_by_user_id:
        :param rel_dockerfile_path:
        :param registry_username:
        :param registry_password:
        :param cluster:
        :param cluster_id:
        :param node_attrs:

        :return: job handle if created with success
        """
        job = Job(
            machine_type=machine_type,
            container=container,
            project_id=project_id,
            name=name,
            command=command,
            ports=ports,
            is_public=is_public,
            workspace=workspace,
            workspace_archive=workspace_archive,
            workspace_url=workspace_url,
            working_directory=working_directory,
            ignore_files=ignore_files,
            experiment_id=experiment_id,
            job_env=job_env,
            use_dockerfile=use_dockerfile,
            is_preemptible=is_preemptible,
            project=project,
            started_by_user_id=started_by_user_id,
            rel_dockerfile_path=rel_dockerfile_path,
            registry_username=registry_username,
            registry_password=registry_password,
            cluster=cluster,
            cluster_id=cluster_id,
            target_node_attrs=node_attrs,
        )
        job_dict = JobSchema().dump(job).data
        return self._create(job_dict, data)

    HOST_URL = config.CONFIG_HOST

    def __init__(self, *args, **kwargs):
        super(JobsClient, self).__init__(*args, **kwargs)
        self.logs_client = http_client.API(config.CONFIG_LOG_HOST,
                                           api_key=self.api_key,
                                           logger=self.logger)

    def delete(self, job_id):
        """

        :param job_id:
        :return:
        """
        url = self._get_action_url(job_id, "destroy")
        response = self.client.post(url)
        return response

    def stop(self, job_id):
        """

        :param job_id:
        :return:
        """
        url = self._get_action_url(job_id, "stop")
        response = self.client.post(url)
        return response

    def list(self, filters):
        return ListJobs(self.client).list(filters=filters)

    def logs(self, job_id, line=0, limit=10000):
        logs = ListJobLogs(self.logs_client).list(job_id=job_id, line=line, limit=limit)
        return logs

    def artifacts_delete(self, job_id, params):
        url = self._get_action_url(job_id, "artifactsDestroy", ending_slash=False)
        response = self.client.post(url, params=params)
        return response

    def artifacts_get(self, job_id):
        url = '/jobs/artifactsGet'
        response = self.client.get(url, params={'jobId': job_id})
        return response

    def artifacts_list(self, filters):
        return ListJobArtifacts(self.client).list(filters=filters)

    def _create(self, job_dict, data):
        """

        :param job_dict:
        :param data:
        :return:
        """
        response = self._get_create_response(job_dict, data)
        return response

    def _get_create_response(self, json_, data):
        """

        :param json_:
        :param data:
        :return:
        """
        return self.client.post("/jobs/createJob/", params=json_, data=data)

    @staticmethod
    def _get_error_message(response):
        try:
            response_data = response.json()
        except ValueError:
            return "Unknown error"

        msg = MessageExtractor().get_message_from_response_data(response_data)
        return msg

    @staticmethod
    def _get_action_url(job_id, action, ending_slash=True):
        template_with_ending_slash = "/jobs/{}/{}/"
        template_without_ending_slash = "/jobs/{}/{}"

        if ending_slash:
            template = template_with_ending_slash
        else:
            template = template_without_ending_slash
        return template.format(job_id, action)
