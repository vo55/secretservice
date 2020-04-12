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

## Output

````bash
2020-04-12 13:38:17 INFO     MAIN: Secret is old and should be rotated. Age: 95 --- <Resource-ID>
2020-04-12 13:38:17 INFO     MAIN: Secret is old and should be rotated. Age: 95 --- <Resource-ID>
2020-04-12 13:38:17 INFO     MAIN: Secret is old and should be rotated. Age: 248 --- <Resource-ID>
2020-04-12 13:38:17 INFO     MAIN: Secret is old and should be rotated. Age: 248 --- <Resource-ID>
2020-04-12 13:38:17 INFO     MAIN: Secret is old and should be rotated. Age: 248 --- <Resource-ID>

