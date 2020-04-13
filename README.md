\[WiP] secretservice for aws
============================
Application to benchmark aws secret handling. Currently a work in progress.

## Installation

Clone this project.

Run in project directory:

```bash
python3 -m pip install .
```

Package scripts shall be available in standard executable locations upon completion.

## Usage Example

Within the project directory:

#### Options
```bash
./secrets-cli -h
```

#### Execution

```bash
./secrets-cli -p my-aws-profile
```

## Rule Overview
#### Old Secrets
If a secret is older than 90 days it should've been rotated already. Often there is fluctuation in teams and the secrets who are meant to be accessed only by team members
are not only known by the team members anymore. Also it prevents being impacted by leaked old secrets.

#### Unused Secrets
Secrets unused for more than 30 days are possibly not used anymore and should be deleted if that's the case.

#### Weak Secrets
Checks some standard policies against the secret to determine how weak a secret is.

## Output

````bash
2020-04-12 13:38:17 INFO     MAIN: Secret is old and should be rotated. Age: 95 --- <Resource-ID>
2020-04-12 13:38:17 INFO     MAIN: Secret is old and should be rotated. Age: 95 --- <Resource-ID>
2020-04-12 13:38:17 INFO     MAIN: Secret is old and should be rotated. Age: 248 --- <Resource-ID>
2020-04-12 13:38:17 INFO     MAIN: Secret is old and should be rotated. Age: 248 --- <Resource-ID>
2020-04-12 13:38:17 INFO     MAIN: Secret is old and should be rotated. Age: 248 --- <Resource-ID>

