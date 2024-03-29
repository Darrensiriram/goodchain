import pickle
from actions import check_balance
from actions import transferCoins
from actions import mining_actions
from database_actions import login
import os
from time import sleep
from utils import helper

poolPath = 'data/pool.dat'
choiceList = ("1", "2", "3", '4', '5', '6', '7')


def print_menu_loggedIn(auth_user, connection):
    cur = connection.cursor()
    result = cur.execute('SELECT username FROM users WHERE id = ?', (auth_user,)).fetchone()
    print(f"Username: {result[0]}")
    print("""
    1 - Transfer Coins
    2 - Check the Balance
    3 - Explore the Chain
    4 - Check the Pool 
    5 - Cancel a transaction
    6 - Mine a Block
    7 - Log out
    """)


def actions(auth_user, connection):
    checkBalanceObject = check_balance.balance(connection, auth_user)
    while True:
        print_menu_loggedIn(auth_user, connection)
        response = input("What would u like to do? \n")
        if response not in choiceList:
            print("Please select a valid option")
            sleep(2)
        elif int(response) == 1 and helper.compare_hashes('data/block.dat'):
            try:
                chosen_user = input("please enter the username: ")
                amount = float(input("please specify the coin amount: "))
                transactionfee = float(input("please enter a transaction fee: "))
                current_balance = checkBalanceObject.get_current_balance_from_user(chosen_user)
                if not current_balance:
                    print("There is no transaction made, Username is not found")
                    sleep(2)
                    continue
            except:
                print("Invalid option")
            else:
                current_balance = checkBalanceObject.current_balance()
                if amount < transactionfee:
                    print("Oops ur amount is smaller then transaction fee")
                    print("Try again....")
                    sleep(2)
                elif current_balance < amount:
                    print("Oops ur balance is smaller then than the amount specified")
                    print("Try again....")
                    sleep(2)
                else:
                    transferCoinsobject = transferCoins.transfercoins(connection, auth_user, chosen_user, amount,
                                                                      transactionfee)
                    tx = transferCoinsobject.createTx(amount, transactionfee)
                    transferCoinsobject.save_transaction_in_the_pool(tx)
                    print("Coins have been transferred")
                continue
        elif int(response) == 2 and helper.compare_hashes('data/block.dat'):
            print(f"Your current balance is: {checkBalanceObject.current_balance()}")
            sleep(2)
            continue
        elif int(response) == 3 and helper.compare_hashes('data/block.dat'):
            print("Explore the chain")
            mining_actions.mine_actions.explore_chain()
            sleep(2)
            continue
        elif int(response) == 4 and helper.compare_hashes('data/block.dat'):
            pool = []
            loadfile = open(poolPath, "rb")
            try:
                while True:
                    data = pickle.load(loadfile)
                    pool.append(data)
            except EOFError:
                pass
            if len(pool) != 0:
                print(pool)
                print(f"Total transactions in the pool: {len(pool)}")
            else:
                print("Pool is empty")
            sleep(4)
        elif int(response) == 5 and helper.compare_hashes('data/block.dat'):
            tcObject = transferCoins.transfercoins(connection, auth_user)
            if transferCoins.transfercoins.cancel_transaction_in_the_pool(tcObject) == False:
                print("Pool is empty")
            else:
                print("Cancel a transaction\n")
                transferCoins.transfercoins.cancel_transaction_in_the_pool(tcObject)
            sleep(2)
            continue
        elif int(response) == 6 and helper.compare_hashes('data/block.dat'):
            loginObject = login.login(connection)
            if transferCoins.transfercoins.get_total_transaction_in_pool() < 5:
                print("There are not enough transaction in the pool.")
                print(f"There are currently {transferCoins.transfercoins.get_total_transaction_in_pool()} in the pool.")
                sleep(2)
            # elif loginObject.get_current_connected_count()[0] < 4:
            #     print("sorry not enough members have valided the chain")
            #     sleep(2)
            elif loginObject.get_current_time():
                print("Whoops u can not mine so fast in a row.")
                sleep(2)
            else:
                print("Let's mine a block")
                specifyBlocks = mining_actions.mine_actions.load_all_transaction_per_block()
                i = 0
                for x in specifyBlocks:
                    print(f"[{i}] : {x}")
                    i += 1
                while True:
                    try:
                        chosenInput = int(input("Please choose a block of transactions: "))
                        if chosenInput == None:
                            break
                        else:
                            if chosenInput < len(specifyBlocks):
                                mining_actions.mine_actions.mine_block(specifyBlocks, chosenInput)
                                mining_actions.mine_actions.save_to_chain(specifyBlocks[0][0])
                                mining_actions.mine_actions.clear_transaction_after_mining(specifyBlocks[0][0])
                                loginObject.set_default_value_connectivity()
                                loginObject.update_time_when_mine()
                                transferCoinsobject = transferCoins.transfercoins(connection, auth_user, "system_user",
                                                                                  25,
                                                                                  0)
                                tx = transferCoinsobject.createSystemTx(25, 0)
                                transferCoinsobject.save_transaction_in_the_pool(tx)
                                checkBalanceObject.update_balance()
                                helper.create_hash('data/block.dat')
                                break
                    except:
                        print("Oops That is not a valid option")
                sleep(2)
            continue
        elif int(response) == 7:
            print("Log out")
            break
