from django.contrib.auth.models import User
from django.db.models import Model
from django.db.models.fields import CharField, DateTimeField, FloatField, IntegerField
from django.db.models.fields.related import ForeignKey, ManyToManyField
from django.utils.translation import ugettext_lazy as _

from village.utils import find_circle_intersections


class Village(Model):
    id = IntegerField(verbose_name=_('village id'), primary_key=True, unique=True, blank=False, null=False)
    name = CharField(max_length=128, verbose_name=_('village name'), unique=True, blank=False, db_index=True)
    x = FloatField(verbose_name=_('coordinate x'))
    y = FloatField(verbose_name=_('coordinate y'))
    created = DateTimeField(verbose_name=_('created'), auto_now=True, auto_now_add=True)
#    owner = ForeignKey(User, verbose_name=_('owner'), db_constraint=False, null=True, blank=True)
    owner = ManyToManyField(User, verbose_name=_('owner'), db_constraint=False, null=True, blank=True)

    def __unicode__(self):
        return u'[%000000000d] %s' % (self.id, self.name)

    class Meta:
        verbose_name = _('village')
        verbose_name_plural = _('villages')
        unique_together = (('x', 'y'),)
        index_together = (('x', 'y'),)


def calculate_villages(a, b, c, a_id, b_id, c_id, ab, bc, ca):
    """
    Calculates three villages and creates three corresponding Village objects.
    Village A becomes the origin.
    Village B is set on X-axis 'ab' units away.
    Village C position is calculated using two circles intersection method.
    Position for village C is chosen randomly between two circle intersection points.
          c
     ca /   \ bc
      /      \
    a ------- b
         ab
    :param a: first village name
    :param b: second village name
    :param c: third village name
    :param ab: distance from first village to second village
    :param bc: distance from second village to third village
    :param ca: distance from third village to first village
    :return: tuple, three calculated Village objects
    """
    intersections = find_circle_intersections(0, 0, ca, ab, 0, bc)
    intersection = intersections[0]
    village_a = Village(id=a_id, name=a, x=0, y=0)
    village_b = Village(id=b_id, name=b, x=ab, y=0)
    village_c = Village(id=c_id, name=c, x=intersection[0], y=intersection[1])
    return village_a, village_b, village_c
