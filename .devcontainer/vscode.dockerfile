# Must build the normal dev image first!
FROM hiveeyes/dev:latest

ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create the non-root user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    #
    # [Optional] Add sudo support. Omit if you don't need to install software after connecting.
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Make Python3.9 the default python (since some extension us /usr/bin/python3)
RUN ln -f -s /usr/local/bin/python3 /usr/bin/python3 && \
    python3 -m pip install -U sphinx rstcheck snooty

# Add docker CLI tools
COPY --from=docker:dind /usr/local/bin/docker /usr/local/bin/