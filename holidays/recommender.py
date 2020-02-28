import redis
from django.conf import settings
from .models import Place

r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=settings.REDIS_DB)

class Recommender(object):
    def get_package_key(self, id):
        return 'package:{}:purchased_with'.format(id)
    
    def packages_bought(self, packages):
        package_ids = [p.id for p in packages]
        for package_id in package_ids:
            for with_id in package_ids:
                if package_id != with_id:
                    r.zincrby(self.get_package_key(package_id),with_id,amount=1)
    
    def suggested_packages_for(self,packages,max_results=6):
        package_ids = [p.id for p in packages]
        if len(packages)==1:
            suggestions=r.zrange(self.get_package_key(package_ids[0]),0,-1,desc=True)[:max_results]
        else:
            flat_ids = ''.join([str(id) for id in package_ids])
            tmp_key = 'tmp_{}'.format(flat_ids)
            key = [self.get_package_key(id) for id in package_ids]
            r.zunionstore(tmp_key,keys)
            r.zrem(tmp_key, *package_ids)
            suggestions = r.zrange(tmp_key,0,-1,desc=True)[:max_results]
            r.delete(tmp_key)
        suggested_packages_ids = [int(id) for id in suggestions]
        suggested_packages = list(Place.objects.filter(id__in=suggested_packages_ids))
        suggested_packages.sort(key=lambda x:suggested_packages_ids.index(x.id))
        return suggested_packages

    def clear_packages(self):
        for id in Place.objects.value_list('id',flat=True):
            r.delete(self.get_package_key(id))
