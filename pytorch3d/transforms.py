import torch
import torch.nn.functional as F


def _skew(v):
    x, y, z = v.unbind(-1)
    zeros = torch.zeros_like(x)
    return torch.stack((
        zeros, -z, y,
        z, zeros, -x,
        -y, x, zeros,
    ), dim=-1).reshape(v.shape[:-1] + (3, 3))


def axis_angle_to_matrix(axis_angle):
    angle = torch.linalg.norm(axis_angle, dim=-1, keepdim=True)
    axis = axis_angle / angle.clamp_min(1e-8)
    k = _skew(axis)
    eye = torch.eye(3, dtype=axis_angle.dtype, device=axis_angle.device)
    eye = eye.expand(axis_angle.shape[:-1] + (3, 3))
    sin = torch.sin(angle)[..., None]
    cos = torch.cos(angle)[..., None]
    return eye + sin * k + (1.0 - cos) * torch.matmul(k, k)


def matrix_to_axis_angle(matrix):
    q = matrix_to_quaternion(matrix)
    return quaternion_to_axis_angle(q)


def quaternion_to_axis_angle(quaternions):
    q = standardize_quaternion(quaternions)
    xyz = q[..., 1:]
    sin_half = torch.linalg.norm(xyz, dim=-1)
    cos_half = q[..., 0]
    angle = 2.0 * torch.atan2(sin_half, cos_half)
    axis = xyz / sin_half[..., None].clamp_min(1e-8)
    return axis * angle[..., None]


def axis_angle_to_quaternion(axis_angle):
    angle = torch.linalg.norm(axis_angle, dim=-1, keepdim=True)
    half = 0.5 * angle
    axis = axis_angle / angle.clamp_min(1e-8)
    return torch.cat((torch.cos(half), axis * torch.sin(half)), dim=-1)


def standardize_quaternion(quaternions):
    return torch.where(quaternions[..., :1] < 0, -quaternions, quaternions)


def quaternion_to_matrix(quaternions):
    q = F.normalize(quaternions, dim=-1)
    r, i, j, k = q.unbind(-1)
    two_s = 2.0
    return torch.stack((
        1 - two_s * (j * j + k * k),
        two_s * (i * j - k * r),
        two_s * (i * k + j * r),
        two_s * (i * j + k * r),
        1 - two_s * (i * i + k * k),
        two_s * (j * k - i * r),
        two_s * (i * k - j * r),
        two_s * (j * k + i * r),
        1 - two_s * (i * i + j * j),
    ), dim=-1).reshape(q.shape[:-1] + (3, 3))


def matrix_to_quaternion(matrix):
    m = matrix
    m00, m01, m02 = m[..., 0, 0], m[..., 0, 1], m[..., 0, 2]
    m10, m11, m12 = m[..., 1, 0], m[..., 1, 1], m[..., 1, 2]
    m20, m21, m22 = m[..., 2, 0], m[..., 2, 1], m[..., 2, 2]

    qw = 0.5 * torch.sqrt((1 + m00 + m11 + m22).clamp_min(0))
    qx = 0.5 * torch.sqrt((1 + m00 - m11 - m22).clamp_min(0))
    qy = 0.5 * torch.sqrt((1 - m00 + m11 - m22).clamp_min(0))
    qz = 0.5 * torch.sqrt((1 - m00 - m11 + m22).clamp_min(0))

    qx = qx * torch.sign(m21 - m12)
    qy = qy * torch.sign(m02 - m20)
    qz = qz * torch.sign(m10 - m01)
    return standardize_quaternion(torch.stack((qw, qx, qy, qz), dim=-1))


def rotation_6d_to_matrix(d6):
    a1, a2 = d6[..., :3], d6[..., 3:6]
    b1 = F.normalize(a1, dim=-1)
    b2 = F.normalize(a2 - (b1 * a2).sum(-1, keepdim=True) * b1, dim=-1)
    b3 = torch.cross(b1, b2, dim=-1)
    return torch.stack((b1, b2, b3), dim=-2)


def matrix_to_rotation_6d(matrix):
    return matrix[..., :2, :].reshape(matrix.shape[:-2] + (6,))


def euler_angles_to_matrix(euler_angles, convention):
    if convention != "XYZ":
        raise NotImplementedError("Only XYZ Euler convention is implemented.")
    x, y, z = euler_angles.unbind(-1)
    cx, cy, cz = torch.cos(x), torch.cos(y), torch.cos(z)
    sx, sy, sz = torch.sin(x), torch.sin(y), torch.sin(z)
    return torch.stack((
        cy * cz, -cy * sz, sy,
        cx * sz + cz * sx * sy, cx * cz - sx * sy * sz, -cy * sx,
        sx * sz - cx * cz * sy, cz * sx + cx * sy * sz, cx * cy,
    ), dim=-1).reshape(euler_angles.shape[:-1] + (3, 3))


def matrix_to_euler_angles(matrix, convention):
    if convention != "XYZ":
        raise NotImplementedError("Only XYZ Euler convention is implemented.")
    sy = matrix[..., 0, 2].clamp(-1, 1)
    y = torch.asin(sy)
    x = torch.atan2(-matrix[..., 1, 2], matrix[..., 2, 2])
    z = torch.atan2(-matrix[..., 0, 1], matrix[..., 0, 0])
    return torch.stack((x, y, z), dim=-1)
