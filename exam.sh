# Exam:
# Reto Kernen, zks252
# Part 1: Data exploration in Unix
# Q1:
# Select only the line that fulfill the iso-code standard and save these lines to a new file
grep -E "^[A-Z]{3}," owid-covid-data.csv > owid-covid-data-filtered.csv

# Q2:
# Count the amount of different iso-codes in the dataset
cut -f1 -d"," owid-covid-data-filtered.csv | uniq -c | wc -l

# Q3:
# Output the month for which we have data (format: YYYY-MM)
cut -f4 -d"," owid-covid-data-filtered.csv | egrep -o "[0-9]{4}-[0-9]{2}" | sort | uniq

# Q4:
# Output the 10 country names (sorted highest first) for which the total number of deaths was highest on 2020-10
grep "2020-10-10" owid-covid-data-filtered.csv | sort -n -k8 -r -t"," | cut -f3 -d","| head

# Q5:
# Output the 10 country names (sorted highest first) for which the total number of deaths per million was highest on 2020-10
grep "2020-10-10" owid-covid-data-filtered.csv | sort -n -k14 -r -t"," | cut -f3 -d","| head
