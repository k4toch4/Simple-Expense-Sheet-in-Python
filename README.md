# Simple-Expense-Sheet-in-Python

Alpha version of a script to administrate an Expense Sheet

This is a code that I make in one day and in a rush, it is simple and chaotic, but it's work great so I wan't to shre with all of you.

I would make some update to this code to create a better version but for now you can use it if you like it

The only thing that you need is the 'pyexcel_ods3' python librery. This script use it to create and manipulate ods file, mainly because I use LibreOffice, but if you use Excel you can change the extensions.

All the code and coments is writting in spanhis, you are welcom to use your own lenguage and modify the code. 

# How to use it

Frist you need to create a json file that is used as a template to create the sheet, in my case I only used four templates: Date, Description, Type and Amount.
If you want tou can modify the config.json file to include more templates. But if yu do this you need to modify the code also (I would work in that in the future).

To create the sheet you need to execute 'init_ods.py'. For now is a separated script and create only a single sheet with a hardcoded name, but in the future I would make some changes here.

After you create the sheet you can add, list and consult the balance in the sheet. 
You can do this using this command:

To add money:
python3 manager.py add [type] "[description]" [money] --fecha [date in  YYY-MM-DD]

To consult balace:
python3 manager.py saldo > This would give you the global balance but you can sort for date using the flags --mes and --anio

To list the information:
python3 manager.py listar --tipo [ingreso o egreso] --descripcion [description] > you can sort from diferent dates using: --fecha-desde [from what date] --fecha-hasta [to a specific date]

Like I said, this is a very sloppy script, but works well, in the future I would update this.
