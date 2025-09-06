.PHONY: all data experiments

data:
	@echo 'Generating Data'
	@echo 'Preparing PEMS-BAY files'
	cd datasets/pemsbay_traffic && ./run.sh
	@echo 'Generating PEMS-BAY train-test splits'
	cd experiments/pemsbay_traffic && python setup_data.py

	@echo 'Generating Data'
	@echo 'Preparing METR-LA files'
	cd datasets/metr-la && ./run.sh
	@echo 'Generating METR-LA train-test splits'
	cd experiments/metr-la && python setup_data.py


experiments:
	@echo 'Running PEMS-BAY experiments'
	cd experiments/pemsbay_traffic && mkdir -p results
	@echo 'Running bayesnewton mean-field model'
	cd experiments/pemsbay_traffic/models && python m_bayes_newt.py 0 1 0
	cd experiments/pemsbay_traffic/models && python m_bayes_newt.py 1 1 0
	cd experiments/pemsbay_traffic/models && python m_bayes_newt.py 2 1 0
	cd experiments/pemsbay_traffic/models && python m_bayes_newt.py 3 1 0
	cd experiments/pemsbay_traffic/models && python m_bayes_newt.py 4 1 0

	@echo 'Running METR-LA experiments'
	cd experiments/metr-la && mkdir -p results
	@echo 'Running bayesnewton mean-field model'
	cd experiments/metr-la/models && python m_bayes_newt.py 0 1 0
	cd experiments/metr-la/models && python m_bayes_newt.py 1 1 0
	cd experiments/metr-la/models && python m_bayes_newt.py 2 1 0
	cd experiments/metr-la/models && python m_bayes_newt.py 3 1 0
	cd experiments/metr-la/models && python m_bayes_newt.py 4 1 0

	


