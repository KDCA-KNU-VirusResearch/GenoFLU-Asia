"""Input accounting regressions; run with python -m unittest discover -s tests."""
import importlib.util
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('genoflu', ROOT / 'genoflu.py')
genoflu = importlib.util.module_from_spec(spec)
spec.loader.exec_module(genoflu)


class InputAccountingTests(unittest.TestCase):
    def setUp(self):
        self.work = tempfile.TemporaryDirectory()
        self.path = Path(self.work.name) / 'batch_alpha.fasta'

    def tearDown(self):
        self.work.cleanup()

    def test_rejects_malformed_inputs(self):
        for text in ['', 'ACGT\n', '>\nACGT\n', '>a|1\n>b|2\nACGT\n',
                     '>a|1\nACGT...\n', '>a|1\nACGT\n>a|1\nACGT\n',
                     '>a name|1\nACGT\n', '>a|1\n---\n']:
            with self.subTest(text=text):
                self.path.write_text(text)
                with self.assertRaises(SystemExit) as caught:
                    genoflu.inspect_fasta(str(self.path))
                self.assertIn(str(self.path), str(caught.exception))

    def test_valid_ambiguity_codes_and_multiline_sequences(self):
        self.path.write_text('>virus|1 description\nacgtN-\nRYSWKMBDHVU\n>virus|2\nACGT\n')
        self.assertEqual(genoflu.inspect_fasta(str(self.path)), ({'virus': 2}, 2))

    def test_zero_hits_keeps_every_input_virus(self):
        self.path.write_text('>first|1\nACGT\n>second|1\nNNNN\n')
        subject = genoflu.GenoFLU(FASTA=str(self.path))
        with patch.object(genoflu, 'run_external'), patch.object(genoflu, 'Blast_Fasta') as blast:
            blast.return_value._raw_lines = []
            subject.blast_hpai_genomes()
        rows = subject.excel_rows()
        self.assertEqual(len(rows), 2)
        self.assertEqual([r['sample'] for r in rows], ['batch_alpha__first', 'batch_alpha__second'])
        self.assertTrue(all(r['Genotype'] == 'Not assigned: No BLAST hits' for r in rows))

    def test_partial_hits_still_keep_no_hit_virus(self):
        self.path.write_text('>first|1\nACGT\n>second|1\nNNNN\n')
        subject = genoflu.GenoFLU(FASTA=str(self.path))
        hit = 'first|1\tACGT\t4\t4\t100\t0\t1e-10\t50\tref\tPB2_group1|ref|PB2'
        with patch.object(genoflu, 'run_external'), patch.object(genoflu, 'Blast_Fasta') as blast:
            blast.return_value._raw_lines = [hit]
            subject.blast_hpai_genomes()
        self.assertEqual(len(subject.excel_rows()), 2)
        self.assertIn('Only 1 segments', subject.results_per_virus['first']['genotype'])
        self.assertEqual(subject.results_per_virus['second']['genotype'], 'Not assigned: No BLAST hits')

    def test_custom_scratch_and_unsafe_path(self):
        with tempfile.TemporaryDirectory(prefix='genoflu_test_', dir='/tmp') as scratch:
            with patch.dict(os.environ, {'GENOFLU_TMPDIR': scratch}):
                with genoflu.blast_workspace() as work:
                    self.assertEqual(Path(work).parent, Path(scratch))
            with patch.dict(os.environ, {'GENOFLU_TMPDIR': scratch + '/with spaces'}):
                with self.assertRaises(SystemExit):
                    genoflu.blast_workspace()


if __name__ == '__main__':
    unittest.main()
