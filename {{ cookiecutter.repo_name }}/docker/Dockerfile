# forcing a linux/amd64 build ensures a generic VM you can create on apple silicon
# the `--platform=linux/amd64` section could be removed if all packages build natively (still causes trouble on osx silicon)
FROM --platform=linux/amd64 condaforge/mambaforge:latest
# ignore this step if using non-linux...
RUN apt update && apt install build-essential -y --no-install-recommends 
RUN mamba install --name base --yes conda-lock --channel conda-forge
COPY --chown=$MAMBA_USER:$MAMBA_USER conda-lock.yml /tmp/conda-lock.yml
RUN mamba lock install /tmp/conda-lock.yml --name {{ cookiecutter.conda_environment }} && \
    mamba clean --all --yes
ARG MAMBA_DOCKERFILE_ACTIVATE=1  # (otherwise python will not be found)
RUN python -c 'import uuid; print(uuid.uuid4())' > /tmp/my_uuid
WORKDIR /{{ cookiecutter.repo_name }}
ENTRYPOINT [ "/bin/bash" ]