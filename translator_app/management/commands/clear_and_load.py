# translator_app/management/commands/clear_and_load.py
import os
import pandas as pd
from django.core.management.base import BaseCommand
from translator_app.models import Translation

class Command(BaseCommand):
    help = "Clear the database and load new words from an Excel file."

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            help='Path to the Excel file containing new words.',
            required=True
        )

    def handle(self, *args, **kwargs):
        file_path = kwargs['file']

        if not os.path.exists(file_path):
            self.stderr.write(f"File not found: {file_path}")
            return

        # Clear the database
        self.stdout.write("Clearing the database...")
        Translation.objects.all().delete()

        # Load new words from the Excel file
        self.stdout.write("Loading new words from the Excel file...")
        df = pd.read_excel(file_path)

        if not {'A', 'B', 'C'}.issubset(df.columns):
            self.stderr.write("The Excel file must contain columns: A (Sheva), B (Adabiy), C (Description).")
            return

        translations = [
            Translation(
                uz_word=row['B'].strip().lower(),
                kh_word=row['A'].strip().lower(),
                description=row['C'].strip()
            )
            for _, row in df.iterrows()
            if pd.notnull(row['A']) and pd.notnull(row['B'])
        ]

        Translation.objects.bulk_create(translations)
        self.stdout.write(f"Successfully loaded {len(translations)} words into the database.")