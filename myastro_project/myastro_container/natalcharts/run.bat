
set original_dir=%CD%
set venv_root_dir="C:\\Users\\User\\Desktop\\myastro\\myastro_project\\myastroenv"
cd %venv_root_dir%
call %venv_root_dir%\Scripts\activate.bat

python C:\\Users\\User\\Desktop\\myastro\\myastro_project\\myastro_container\\manage.py update_daily
call %venv_root_dir%\Scripts\deactivate.bat
cd %original_dir%
exit /B 1

