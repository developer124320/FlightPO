'''
Created on Jan 20, 2015

@author: KangKuk
'''
import define

class Obstacle(object):
    '''
    classdocs
    '''

#         public Obstacle(string string_0, Point3d point3d_0, double double_0, double double_1, double double_2, ObstacleType obstacleType_0, long long_0, object object_0)
#         {
#             self.name = string_0;
#             self.position = point3d_0;
#             self.trees = double_0;
#             self.tolerance = double_1;
#             self.Type = obstacleType_0;
#             self.mocMultiplier = double_2;
#             self.layerId = long_0;
#             self.featureId = object_0;
#             self.assigned = true;
#         }

    def __init__(self, name, position, layerId, featureId, area, trees = 0.0, mocMultiplier = 1, tolerance = 20.0, obstacleType = "node"):
        '''
        Constructor
        '''
        self.name = name;
        self.position = position
        self.trees = trees; # Default:30.0
        self.tolerance = tolerance
        self.Type = obstacleType
        self.mocMultiplier = mocMultiplier # Default:2
        self.layerId = layerId
        self.featureId = featureId
        self.area = area
        self.result = {}
        self.assigned = True
        self.positionDegree = None
        self.oca = 0.0
#         public void method_0(string string_0, Point3d point3d_0, double double_0, double double_1, double double_2, ObstacleType obstacleType_0, long long_0)
#         {
#             self.name = string_0;
#             self.position = point3d_0;
#             self.trees = double_0;
#             self.tolerance = double_1;
#             self.mocMultiplier = double_2;
#             self.Type = obstacleType_0;
#             self.layerId = long_0;
#             self.assigned = true;
#         }
# 
    def method_0(self, name, position, trees, tolerance, obstacleType, mocMultiplier, objectId):
        self.name = name;
        self.position = position;
        self.trees = trees;
        self.tolerance = tolerance;
        self.Type = obstacleType;
        self.mocMultiplier = mocMultiplier;
        self.layerId = objectId;
        self.assigned = True;

#         public void method_1(string string_0, Point3d point3d_0, double double_0, double double_1, double double_2, ObstacleType obstacleType_0, long long_0, object object_0)
#         {
#             self.name = string_0;
#             self.position = point3d_0;
#             self.trees = double_0;
#             self.tolerance = double_1;
#             self.mocMultiplier = double_2;
#             self.Type = obstacleType_0;
#             self.layerId = long_0;
#             self.featureId = object_0;
#             self.assigned = true;
#         }
    def method_1(self, name, position, trees, tolerance, obstacleType, mocMultiplier, objectId, tag = None):
        self.name = name;
        self.position = position;
        self.trees = trees;
        self.tolerance = tolerance;
        self.Type = obstacleType;
        self.mocMultiplier = mocMultiplier;
        self.layerId = objectId;
        self.featureId = tag;
        self.assigned = True;
# 
#         public void method_2()
#         {
#             self.assigned = false;
#         }
# 
    def method_2(self):
        self.assigned = False
#         private long getMOC()
#         {
#             object[] x = new object[] { self.name, self.position.get_X(), self.position.get_Y(), self.position.get_Z(), self.trees, self.tolerance, self.Type, self.mocMultiplier };
#             string str = string.Format("{0}{1}{2}{3}{4}{5}{6}{7}", x);
#             string str1 = str.Substring(0, str.Length / 2);
#             string str2 = str.Substring(str.Length / 2);
#             byte[] bytes = BitConverter.GetBytes(str1.GetHashCode());
#             byte[] numArray = BitConverter.GetBytes(str2.GetHashCode());
#             return (long)((ulong)bytes[0] << 56 | (ulong)bytes[1] << 48 | (ulong)bytes[2] << 40 | (ulong)bytes[3] << 32 | (ulong)numArray[0] << 24 | (ulong)numArray[1] << 16 | (ulong)numArray[2] << 8 | (ulong)numArray[3]);
#         }
# 
    def getMOC(self):
        x = [ self.name, self.position.get_X(), self.position.get_Y(), self.position.get_Z(), self.trees, self.tolerance, self.Type, self.mocMultiplier ]
        result = "{0[0]}{0[1]}{0[2]}{0[3]}{0[4]}{0[5]}{0[6]}{0[7]}".format(x)
        
        return result

    def __str__(self, *args, **kwargs):
        x = [self.name, self.position.get_X(), self.position.get_Y(), self.position.get_Z(), self.tolerance, self.trees, self.Type]
        return "Name: {0[0]}, Position: {0[1]:0.2},{0[2]:0.2},{0[3]:0.2}, Tolerance: {0[4]}, Trees: {0[5]}, Type: {0[6]}".format(x)
    
    def get_Position(self):
        if define._units == 0:
            return self.position
        else:
            return self.positionDegree
    Position = property(get_Position, None, None, None)
    
    def get_Tolerance(self):
        return self.tolerance
    Tolerance = property(get_Tolerance, None, None, None)
    
    def get_Trees(self):
        return self.trees
    Trees = property(get_Trees, None, None, None)

    def get_Name(self):
        return self.name
    Name = property(get_Name, None, None, None)

    def get_assigned(self):
        return self.assigned
    Assigned = property(get_assigned, None, None, None)

    def get_MocMultiplier(self):
        return self.mocMultiplier
    MocMultiplier = property(get_MocMultiplier, None, None, None)
    
#         public override string ToString()
#         {
#             if (!self.assigned)
#             {
#                 return "";
#             }
#             string oBSTACLEFORMAT = Formating.OBSTACLE_FORMAT;
#             object[] x = new object[] { self.name, self.position.get_X(), self.position.get_Y(), self.position.get_Z(), self.tolerance, self.trees, self.Type };
#             return string.Format(oBSTACLEFORMAT, x);
#         }
#     }

class IObstacleEvaluator:
    def imethod_0(self, obstacle_0):
        pass
class BaroVnavCriticalObstacle:
    def __init__(self, obstacle_0, eqAltitude, oca, och, baroVnavSurfaceType):
        '''
        Obstacle obstacle_0, double eqAltitude, double oca, BaroVNAV.BaroVnavSurfaceType baroVnavSurfaceType
        '''
        self.obstacle = obstacle_0
        self.eqAltitude = eqAltitude
        self.baroVnavSurfaceType = baroVnavSurfaceType
        self.oca = oca
        self.och = och

    def assign(self, obstacle_0, eqAltitude, oca, och, baroVnavSurfaceType):
        '''
        Obstacle obstacle_0, double eqAltitude, double oca, BaroVNAV.BaroVnavSurfaceType baroVnavSurfaceType
        '''
        if oca < self.oca:
            return
        self.obstacle = obstacle_0
        self.eqAltitude = eqAltitude
        self.baroVnavSurfaceType = baroVnavSurfaceType
        self.oca = oca
        self.och = och
    def getOCH(self):
        return self.och
        