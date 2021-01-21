from data.DataRepository import DataRepository
# DataRepository.insertscore("klaas", 5.483, 1)
# DataRepository.insertscore("klaas", 7.153, 1)
# DataRepository.insertscore("klaas", 4.948, 1)
data = DataRepository.getscoreboard(1)
print(data)
data = DataRepository.readgames()
print(data)
