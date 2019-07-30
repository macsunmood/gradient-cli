from . import base_client
from .. import models, repositories


class HyperparameterJobsClient(base_client.BaseClient):
    def create(
            self,
            name,
            project_id,
            tuning_command,
            worker_container,
            worker_machine_type,
            worker_command,
            worker_count,
            is_preemptible=True,
            ports=None,
            workspace_url=None,
            artifact_directory=None,
            cluster_id=None,
            experiment_env=None,
            trigger_event_id=None,
            model_type=None,
            model_path=None,
            dockerfile_path=None,
            registry_username=None,
            registry_password=None,
            container_user=None,
            working_directory=None,
            use_dockerfile=False,
    ):
        """Create hyperparameter tuning job

        :param str name: Name of new experiment [required]
        :param str project_id: Project ID [required]
        :param str tuning_command: Tuning command [required]
        :param str worker_container: Worker container  [required]
        :param str worker_machine_type: Worker machine type  [required]
        :param str worker_command: Worker command  [required]
        :param int worker_count: Worker count  [required]
        :param bool is_preemptible: Flag: is preemptible
        :param list[str] ports: Port to use in new experiment
        :param str workspace_url: Project git repository url
        :param str artifact_directory: Artifacts directory
        :param str cluster_id: Cluster ID
        :param dict experiment_env: Environment variables (in JSON)
        :param str trigger_event_id: GradientCI trigger event id
        :param str model_type: Model type
        :param str model_path: Model path
        :param str dockerfile_path: Path to dockerfile in project
        :param str registry_username: Hyperparameter server registry username
        :param str registry_password: Hyperparameter server registry password
        :param str container_user: Hyperparameter server container user
        :param str working_directory: Working directory for the experiment
        :param bool use_dockerfile: Flag: use dockerfile

        :returns: ID of a new job
        :rtype: str
        """

        hyperparameter = models.Hyperparameter(
            name=name,
            project_id=project_id,
            tuning_command=tuning_command,
            worker_container=worker_container,
            worker_machine_type=worker_machine_type,
            worker_command=worker_command,
            worker_count=worker_count,
            is_preemptible=is_preemptible,
            ports=ports,
            workspace_url=workspace_url,
            artifact_directory=artifact_directory,
            cluster_id=cluster_id,
            experiment_env=experiment_env,
            trigger_event_id=trigger_event_id,
            model_type=model_type,
            model_path=model_path,
            dockerfile_path=dockerfile_path,
            registry_username=registry_username,
            registry_password=registry_password,
            container_user=container_user,
            working_directory=working_directory,
            use_dockerfile=use_dockerfile,
        )

        handle = repositories.CreateHyperparameterJob(client=self.client).create(hyperparameter)
        return handle

    def run(
            self,
            name,
            project_id,
            tuning_command,
            worker_container,
            worker_machine_type,
            worker_command,
            worker_count,
            is_preemptible=True,
            ports=None,
            workspace_url=None,
            artifact_directory=None,
            cluster_id=None,
            experiment_env=None,
            trigger_event_id=None,
            model_type=None,
            model_path=None,
            dockerfile_path=None,
            registry_username=None,
            registry_password=None,
            container_user=None,
            working_directory=None,
            use_dockerfile=False,
    ):
        """Create and start hyperparameter tuning job

        *EXAMPLE*::

            gradient hyperparameters run
            --name HyperoptKerasExperimentCLI1
            --projectId <your-project-id>
            --tuningCommand 'make run_hyperopt'
            --workerContainer tensorflow/tensorflow:1.13.1-gpu-py3
            --workerMachineType K80
            --workerCommand 'make run_hyperopt_worker'
            --workerCount 2
            --workspaceUrl git+https://github.com/Paperspace/hyperopt-keras-sample


        :param str name: Name of new experiment  [required]
        :param str project_id: Project ID  [required]
        :param str tuning_command: Tuning command  [required]
        :param str worker_container: Worker container  [required]
        :param str worker_machine_type: Worker machine type  [required]
        :param str worker_command: Worker command  [required]
        :param str worker_count: Worker count  [required]
        :param bool is_preemptible: Flag: is preemptible
        :param list[str] ports: Port to use in new experiment
        :param str workspace_url: Project git repository url
        :param str artifact_directory: Artifacts directory
        :param str cluster_id: Cluster ID
        :param dict experiment_env: Environment variables (in JSON)
        :param str trigger_event_id: GradientCI trigger event id
        :param str model_type: Model type
        :param str model_path: Model path
        :param str dockerfile_path: Path to dockerfile
        :param str registry_username: container registry username
        :param str registry_password: container registry password
        :param str container_user: container user
        :param str working_directory: Working directory for the experiment
        :param bool use_dockerfile: Flag: use dockerfile

        :returns: ID of a new job
        :rtype: str
        """

        hyperparameter = models.Hyperparameter(
            name=name,
            project_id=project_id,
            tuning_command=tuning_command,
            worker_container=worker_container,
            worker_machine_type=worker_machine_type,
            worker_command=worker_command,
            worker_count=worker_count,
            is_preemptible=is_preemptible,
            ports=ports,
            workspace_url=workspace_url,
            artifact_directory=artifact_directory,
            cluster_id=cluster_id,
            experiment_env=experiment_env,
            trigger_event_id=trigger_event_id,
            model_type=model_type,
            model_path=model_path,
            dockerfile_path=dockerfile_path,
            registry_username=registry_username,
            registry_password=registry_password,
            container_user=container_user,
            working_directory=working_directory,
            use_dockerfile=use_dockerfile,
        )

        handle = repositories.CreateAndStartHyperparameterJob(client=self.client).create(hyperparameter)
        return handle

    def get(self, id_):
        """Get Hyperparameter tuning job's instance

        :param str id_: Hyperparameter job id

        :returns: instance of Hyperparameter
        :rtype: models.Hyperparameter
        """
        job = repositories.GetHyperparameterTuningJob(self.client).get(id=id_)
        return job

    def start(self, id_):
        """Start existing hyperparameter tuning job

        :param str id_: Hyperparameter job id
        :raises: exceptions.GradientSdkError
        """
        repositories.StartHyperparameterTuningJob(self.client).start(id_=id_)

    def list(self):
        """Get a list of hyperparameter tuning jobs

        *EXAMPLE*::

            gradient hyperparameters list

        *EXAMPLE RETURN*::

            +--------------------------------+----------------+------------+
            | Name                           | ID             | Project ID |
            +--------------------------------+----------------+------------+
            | name-of-your-experiment-job    | job-id         | project-id |
            | name-of-your-experiment-job    | job-id         | project-id |
            | name-of-your-experiment-job    | job-id         | project-id |
            | name-of-your-experiment-job    | job-id         | project-id |
            | name-of-your-experiment-job    | job-id         | project-id |
            +--------------------------------+----------------+------------+


        :rtype: list[models.Hyperparameter]
        """
        experiments = repositories.ListHyperparameterJobs(self.client).list()
        return experiments
