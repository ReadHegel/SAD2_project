for i in {1..5}; do
    echo "=== RUN $i ==="
    export RANDOM_SEED=$i
    ./all_script.sh
    rm all_data_run_$i.csv
    cp all_data.csv all_data_run_$i.csv
    echo "=== END RUN $i ==="
done
rm all_data.csv