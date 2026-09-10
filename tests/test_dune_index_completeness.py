from src.data.dune import DuneError
from src.indexer import dune_index as module
from src.models import VerifiedPool
import pytest


def test_failed_transfer_does_not_overwrite_existing_artifacts(tmp_path, monkeypatch):
    sentinel = tmp_path / 'transfers.json'
    sentinel.write_text('[{"retained": true}]')
    def query(name, **kwargs):
        if name == 'transfers':
            raise DuneError('unavailable')
        return []
    monkeypatch.setattr(module, 'query', query)
    with pytest.raises(DuneError, match='existing artifacts preserved'):
        module.index_events_from_dune([], '0x'+'11'*20, 1, 2, tmp_path)
    assert sentinel.read_text() == '[{"retained": true}]'
    assert not (tmp_path / 'swaps.json').exists()


def test_all_verified_v4_pools_are_queried(tmp_path, monkeypatch):
    pools = [VerifiedPool(chain_id=1,protocol='uniswap',version='v4',architecture='singleton',factory_address='',pool_address='0x'+format(i,'064x'),verified=True) for i in range(1,97)]
    seen=[]
    def query(name, **kwargs):
        if name == 'liquidity_uniswap_v4_modify':
            seen.extend(kwargs['pool_id_list'])
        return []
    monkeypatch.setattr(module,'query',query)
    module.index_events_from_dune(pools,'0x'+'11'*20,1,2,tmp_path,index_token_transfer=False)
    assert sorted(seen)==sorted(p.pool_address for p in pools)
