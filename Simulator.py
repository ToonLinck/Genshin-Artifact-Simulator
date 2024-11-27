import Artifact_Generator as artGen

DOMAIN = 'Domain'
STRONGBOX = 'Strongbox'

domain_runs = 5000
artifact_count = 0
final_artifacts = []
counter = 0

for i in range(domain_runs):
    artifact_count += artGen.domain_run()

for i in range(artifact_count):
    artifact = artGen.generate_artifact(DOMAIN)
    if artifact[artGen.SET] == 1:
        if artifact[artGen.SLOT] != 'Circlet':
            if 'CR' in artifact[artGen.SUBSTATS] and 'CD' in artifact[artGen.SUBSTATS]:
                counter += 1
        else:
            if artifact[artGen.MAIN_STAT] == 'CR' or artifact[artGen.MAIN_STAT] == 'CD':
                if 'CR' in artifact[artGen.SUBSTATS] or 'CD' in artifact[artGen.SUBSTATS]:
                    counter += 1

print(f"No. of Domain Runs: {domain_runs}")
print(f"No. of Artifacts: {artifact_count}")
print(f"No. of double Crit Artifacts: {counter}")
print(f"Ratio: {(counter / domain_runs) * 100}%")
#for c in range(counter):
#    artGen.print_result(final_artifacts[c])